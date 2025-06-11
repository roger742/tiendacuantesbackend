from django import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RolViewSet, UsuarioViewSet, CategoriaViewSet
from . import views

router = DefaultRouter()

#A esto no le muevan bola de nacos
urlpatterns = [
    #-----------------------------------------------------------------------------------------------------------------------#
    path('super/', include(router.urls)),
    # Paths: login/home
    path('', views.login_view, name='login'),
    # Paths: logout
    path('logout/', views.logout_view, name='logout'),

    # Paths: Cuenta: Home
    path('cuenta/<int:user_id>/', views.CuentaHome, name='cuentaHome'),
    # Paths Cuenta: direccion
    path('cuenta/direcciones/agregar/<int:user_id>', views.crearDireccion, name='crearDireccion'),

    #-----------------------------------------------------------------------------------------------------------------------#
    # Paths: Vendedor
    path('homeVendedor/', views.homeVendedor, name='homeVendedor'),  
    # Paths: Vendedor: Registro
    path('registroVendedor/', views.registro_vendedor_view, name='registro_vendedor'),
    path('api/registrar_vendedor/', views.registrar_vendedor, name='registrar_vendedor'),
    # Paths: Vendedor: home
    path('inicioProductosVendedor/', views.inicioProductosVendedor, name='inicioProductosVendedor'),
    # Paths: Vendedor: pedidos: home
    path('inicioPedidosVendedor/', views.inicioPedidosVendedor, name='inicioPedidosVendedor'),
    # Paths: Vendedor: productos: create
    path('crearProductoVendedor/', views.crearProductoVendedor, name='crearProductoVendedor'),
    # Paths: Vendedor: productos: eliminar
    path('eliminarProductoVendedor/<int:producto_id>/', views.eliminarProductoVendedor, name='eliminarProductoVendedor'),
    # Paths: Vendedor: productos: modificar
    path('modificarProductoVendedor/<int:producto_id>/', views.modificarProductoVendedor, name='modificarProductoVendedor'),
    path('gestionarProductoVendedor/', views.gestionarProductoVendedor, name='gestionarProductoVendedor'),

    #-----------------------------------------------------------------------------------------------------------------------#
    # Paths: Administracion:
    path('homeAdmin/', views.homeAdmin, name='homeAdmin'),

    # Paths: Administracion: Clientes: home 
    path('inicioClientesAdmin/', views.inicioClientesAdmin, name='inicioClientesAdmin'),
    # Paths: Administracion: Clientes: consulta
    path('gestionarClientesAdmin/', views.gestionar_clientes_admin, name='gestionarClientesAdmin'),
    # Paths: Administracion: Clientes: drop
    path('eliminarClientesAdmin/<int:cliente_id>/', views.eliminarClientesAdmin, name='eliminarClientesAdmin'),

    # Paths: Administracion: Vendedor: home
    path('inicioVendedorAdmin/', views.inicioVendedorAdmin, name='inicioVendedorAdmin'),
    # Paths: Administracion: Vendedor: consulta
    path('gestionarVendedorAdmin/', views.gestionarVendedorAdmin, name='gestionarVendedorAdmin'),

    # Paths: Administracion: Categorias: home
    path('inicioCategoriasAdmin/', views.inicioCategoriasAdmin, name='inicioCategoriasAdmin'),
    # Paths: Administracion: Categorias: create
    path('crearCategoriaAdmin/', views.crearCategoriaAdmin, name='crearCategoriaAdmin'),
    # Paths: Administracion: Categorias: consulta
    path('gestionarCategoriasAdmin/', views.gestionarCategoriasAdmin, name='gestionarCategoriasAdmin'),
    # Paths: Administracion: Categorias: update
    path('modificarCategoriasAdmin/<int:categoria_id>/', views.modificarCategoriasAdmin, name='modificarCategoriasAdmin'),
    # Paths: Administracion: Categorias: drop
    path('eliminarCategoriaAdmin/<int:categoria_id>/', views.eliminarCategoriaAdmin, name='eliminarCategoriaAdmin'),

    # Paths: Administracion: Productos: home
    path('inicioProductosAdmin/', views.inicioProductosAdmin, name='inicioProductosAdmin'),
    # Paths: Administracion: Productos: consulta
    path('gestionarProductosAdmin/', views.gestionarProductosAdmin, name='gestionarProductosAdmin'),

    # Paths: Administracion: Pedidos: home
    path('inicioPedidosAdmin/', views.inicioPedidosAdmin, name='inicioPedidosAdmin'),
    path('detallePedidoAdmin/<int:pedido_id>/', views.detallePedidoAdmin, name='detallePedidoAdmin'),
    #-----------------------------------------------------------------------------------------------------------------------#
    # Paths: Cliente
    path('home/', views.homeCliente, name='homeCliente'), 
    # Paths: Cliente: registro:           
    path('registroCliente/', views.registro_clientes_view, name='registro_clientes'),       #URL para entrar al registro de clientes
    path('api/registrar_cliente/', views.registrar_cliente, name='registrar_cliente'),
    # Paths: Cliente: Pedidos: Home
    path('ClientePedidosHome/', views.ClientePedidosHome, name='ClientePedidosHome'),

    #-----------------------------------------------------------------------------------------------------------------------#
    # Paths: Carrito
    path('carrito/agregar/<int:producto_id>/', views.agregar_a_carrito, name='agregar_a_carrito'),
    path('carrito/', views.ver_carrito, name='carrito'),
    path('carrito/eliminar/<int:item_id>/', views.eliminar_del_carrito, name='remove_from_cart'),
    path('ClienteProductoHome/', views.seguir_comprando, name='seguir-comprando'),
    path('carrito/actualizar/<int:item_id>/', views.actualizar_cantidad, name='actualizar_cantidad'),
    
    #-----------------------------------------------------------------------------------------------------------------------#
    # Paths: Pedido: Cliente
    path('pedidos/<int:user_id>', views.verPedido, name='verPedido'),
    # Paths: Pedido: Crear Pedido
    path('procesar_compra/<int:user_id>', views.crear_pedido, name='crear_pedido'),
    # Paths: Pedido: Pedido Confirmado
    path('pedidos/confirmar/<int:user_id>', views.confirmar_pedido, name='confirmar_pedido'),
    # Paths: Pedido: Detalles
    path('pedido/<int:pedido_id>/detalles/<int:user_id>/', views.ver_detalles_pedido, name='verPedidoDetalles'),
    # Paths: Pedido: Cliente: Cancelar
    path('pedidos/cancelar/<int:pedido_id>/', views.cancelar_pedido, name='cancelarPedido'),

    path('prueba/', views.prueba_confirmar_pedido, name='prueba_confirmar_pedido')
]