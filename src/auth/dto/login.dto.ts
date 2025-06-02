import { IsNotEmpty } from 'class-validator';

export class LoginDto {
  @IsNotEmpty()
  usuario: string;

  @IsNotEmpty()
  contraseña: string;
}
