import { BadRequestException, Injectable, NotFoundException } from '@nestjs/common';
import { CreateProductDto } from './dto/create-product.dto';
import { UpdateProductDto } from './dto/update-product.dto';
import { Product } from './entities/product.entity';
import { Repository } from 'typeorm';
import { InjectRepository } from '@nestjs/typeorm';
import { Category } from 'src/categories/entities/category.entity';

@Injectable()
export class ProductsService {
  constructor(
    @InjectRepository(Product)
    private readonly productRepository: Repository<Product>,

    @InjectRepository(Category)
    private readonly categoryRepository: Repository<Category>,
  ) {}

  async create(createProductDto: CreateProductDto) {
    const category = await this.categoryRepository.findOneBy({
      name: createProductDto.category,
    });

    if (!category) {
      throw new BadRequestException('La categoría no existe');
    }

    return await this.productRepository.save({
      ...createProductDto,
      category,
    });
  }

  async findAll() {
    return await this.productRepository.find({
      relations: ['category'],
    });
  }

  async findOne(id: number) {
    const product = await this.productRepository.findOne({
      where: { id },
      relations: ['category'],
    });

    if (!product) {
      throw new NotFoundException(`Producto con ID ${id} no encontrado`);
    }

    return product;
  }

  async update(id: number, updateProductDto: UpdateProductDto) {
    const product = await this.productRepository.findOneBy({ id });
  
    if (!product) {
      throw new NotFoundException(`Producto con ID ${id} no encontrado`);
    }
  
    let category;
    if (updateProductDto.category) {
      category = await this.categoryRepository.findOneBy({
        name: updateProductDto.category,
      });
  
      if (!category) {
        throw new BadRequestException('Categoría no válida');
      }
    }
  
    return await this.productRepository.save({
      ...product,
      ...updateProductDto,
      category,
    });
  }
  

  async remove(id: number) {
    const product = await this.productRepository.findOneBy({ id });

    if (!product) {
      throw new NotFoundException(`Producto con ID ${id} no encontrado`);
    }

    return await this.productRepository.remove(product);
  }
}
