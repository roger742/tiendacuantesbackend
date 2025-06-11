from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Rol, Categoria, Producto, Carrito, CarritoItems, Pedido, DetallePedido, Direccion

admin.site.register(Carrito)
admin.site.register(CarritoItems)
admin.site.register(DetallePedido)
admin.site.register(Pedido)
admin.site.register(Direccion)

@admin.register(Usuario)
class CustomUserAdmin(UserAdmin):
    # Configuración de los campos que se muestran en el admin
    fieldsets = (
        (None, {'fields': ('usuario', 'password')}),
        ('Información personal', {'fields': ('nombre', 'aPaterno', 'aMaterno', 'correo', 'telefono')}),
        ('Permisos', {'fields': ('is_staff', 'is_superuser', 'is_active', 'rol')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('usuario', 'correo', 'nombre', 'aPaterno', 'aMaterno', 'password1', 'password2', 'rol', 'is_staff', 'is_superuser'),
        }),
    )
    # Campos que se muestran en la lista de usuarios
    list_display = ('usuario', 'correo', 'nombre', 'is_staff', 'is_active', 'rol')
    search_fields = ('usuario', 'correo', 'nombre')
    ordering = ('usuario',)

    # Quita configuraciones que no se aplican a tu modelo
    filter_horizontal = ()  # Sin relación con 'groups' o 'user_permissions'
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'rol')  # Ajustar según tus campos

# Registro de los modelos restantes
@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')
    search_fields = ('nombre', 'descripcion')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    # Campos que se muestran en la lista de productos
    list_display = ('id', 'nombre', 'descripcion', 'costo', 'stock', 'categoria', 'usuario', 'is_active')
    # Campos que puedes buscar en el panel de administración
    search_fields = ('nombre', 'descripcion', 'categoria__nombre', 'usuario__usuario')
    # Filtros para facilitar la búsqueda en el panel de administración
    list_filter = ('categoria', 'usuario', 'stock')
    # Orden de los productos en la lista de administración
    ordering = ('nombre',)
    # Campos que se mostrarán en los formularios del admin para modificar un producto
    fieldsets = (
        (None, {'fields': ('nombre', 'descripcion', 'costo', 'stock', 'categoria', 'usuario', 'is_active')}),
    )
    # En el caso de agregar un producto, se mostrarán estos campos
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nombre', 'descripcion', 'costo', 'stock', 'categoria', 'usuario', 'is_active'),
        }),
    )