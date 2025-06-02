import { IsNotEmpty, IsOptional, IsEnum, IsString } from 'class-validator';

export class RegisterDto {
  @IsNotEmpty()
  nombre: string;

  @IsNotEmpty()
  usuario: string;

  @IsNotEmpty()
  contraseña: string;

  @IsEnum(['jefe', 'empleado', 'cliente'])
rol: 'jefe' | 'empleado' | 'cliente';

  @IsOptional()
  puesto?: string;

  @IsOptional()
  fecha_ingreso?: string;
}

