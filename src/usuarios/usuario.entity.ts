import { Entity, Column, PrimaryGeneratedColumn } from 'typeorm';

@Entity('usuarios')
export class Usuario {
  @PrimaryGeneratedColumn()
  id_usuario: number;

  @Column()
  nombre: string;

  @Column({ unique: true })
  usuario: string;

  @Column()
  contraseña: string;

 @Column({ type: 'enum', enum: ['jefe', 'empleado', 'cliente'] })
  rol: 'jefe' | 'empleado' | 'cliente';


  @Column({ default: true })
  estado: boolean;

  @Column({ nullable: true })
  puesto?: string;

  @Column({ type: 'date', nullable: true })
  fecha_ingreso?: string;
}
