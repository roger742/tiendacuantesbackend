import { Entity, Column, OneToMany, DeleteDateColumn } from 'typeorm';
import { Product } from '../../products/entities/product.entity';

@Entity('categories')
export class Category {
  @Column({ primary: true, generated: true })
  id: number;

  @Column({ type: 'varchar', length: 255, nullable: false })
  name: string;

  @OneToMany(() => Product, (product) => product.category)
  products: Product[];

  @DeleteDateColumn()
  deletedAt: Date;
}
