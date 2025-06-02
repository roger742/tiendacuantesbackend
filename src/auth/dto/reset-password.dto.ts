import { IsNotEmpty } from 'class-validator';

export class ResetPasswordDto {
  @IsNotEmpty()
  usuario: string;

  @IsNotEmpty()
  nuevaContraseña: string;
}
