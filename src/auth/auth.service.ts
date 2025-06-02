import { Injectable, UnauthorizedException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Usuario } from '../usuarios/usuario.entity';
import { Repository } from 'typeorm';
import * as bcrypt from 'bcrypt';
import { JwtService } from '@nestjs/jwt';
import { RegisterDto } from './dto/register.dto';

@Injectable()
export class AuthService {
  constructor(
    @InjectRepository(Usuario)
    private usuarioRepo: Repository<Usuario>,
    private jwtService: JwtService,
  ) {}

  async register(dto: RegisterDto) {
  const usuarioExistente = await this.usuarioRepo.findOne({
    where: { usuario: dto.usuario },
  });
  if (usuarioExistente) {
    throw new Error('El nombre de usuario ya existe');
  }

  const hash = await bcrypt.hash(dto.contraseña, 10);
  const nuevoUsuario = this.usuarioRepo.create({ ...dto, contraseña: hash });

  return this.usuarioRepo.save(nuevoUsuario);
}

  async login(usuario: string, contraseña: string) {
    const user = await this.usuarioRepo.findOne({ where: { usuario } });
    if (!user) throw new UnauthorizedException('Usuario no encontrado');

    const valido = await bcrypt.compare(contraseña, user.contraseña);
    if (!valido) throw new UnauthorizedException('Contraseña incorrecta');

    const payload = { sub: user.id_usuario, usuario: user.usuario, rol: user.rol };
    const token = this.jwtService.sign(payload);

    return {
      access_token: token,
      usuario: {
        id: user.id_usuario,
        nombre: user.nombre,
        rol: user.rol,
      },
    };

    
  }
  async resetPassword(usuario: string, nuevaContraseña: string) {
  const user = await this.usuarioRepo.findOne({ where: { usuario } });

  if (!user) {
    throw new Error('Usuario no encontrado');
  }

  const nuevaHash = await bcrypt.hash(nuevaContraseña, 10);
  user.contraseña = nuevaHash;

  await this.usuarioRepo.save(user);

  return { mensaje: 'Contraseña actualizada correctamente' };
}

}

