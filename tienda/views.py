from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Rol, Usuario, Categoria, Producto, Carrito, CarritoItems, Direccion, Pedido, DetallePedido
from .serializers import RolSerializer, UsuarioSerializer, CategoriaSerializer, ProductoSerializer, DireccionSerializer
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.db.models import Count, Q
from django.utils import timezone

# ViewSet para el modelo Rol
class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    permission_classes = [IsAuthenticated]

# ViewSet para el modelo Usuario
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]

# ViewSet para el modelo Categoria
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]

# ViewSet para el modelo Producto
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer


# Vista logout
def logout_view(request):
    logout(request)
    return redirect('login')

# Vista login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Aquí verificamos el rol del usuario y redirigimos según el rol
            if user.rol.nombre == 'administrador':
                return redirect('homeAdmin')  # Redirige al home de administrador
            elif user.rol.nombre == 'vendedor':
                return redirect('homeVendedor')  # Redirige al home de vendedor
            elif user.rol.nombre == 'cliente':
                return redirect('homeCliente')  # Redirige al home de cliente
            else:
                return redirect('login')  # Si no tiene un rol válido, redirige al login

    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Vista Cuenta: home
def CuentaHome(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)
    direcciones = Direccion.objects.filter(usuario=usuario)
    direccion_principal = direcciones.filter(es_principal=True).first()  # Obtiene la dirección principal, si existe
    return render(request, 'cuenta/homeCuenta.html', {
        'usuario': usuario,
        'direcciones': direcciones,
        'direccion_principal': direccion_principal,
        'selected_direccion_id': direccion_principal.id if direccion_principal else None
    })

# Vista Cuenta: direccion
def crearDireccion(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)
    # Verificar que la solicitud sea POST
    if request.method == 'POST':
        usuario = request.user  # Asumiendo que el usuario autenticado está relacionado con el modelo `Usuario`
        
        # Obtener los datos del formulario
        codigo_postal = request.POST.get('codigoPostal')
        calle = request.POST.get('calle')
        no_ext = request.POST.get('noExt')
        referencia = request.POST.get('referencia')
        ciudad = request.POST.get('ciudad')
        estado = request.POST.get('estado')
        es_principal = request.POST.get('es_principal') == 'True'

        # Si la dirección es principal, desmarcar las demás direcciones principales del usuario
        if es_principal:
            Direccion.objects.filter(usuario=usuario, es_principal=True).update(es_principal=False)

        # Crear la nueva dirección
        nueva_direccion = Direccion(
            usuario=usuario,
            codigoPostal=codigo_postal,
            calle=calle,
            noExt=no_ext,
            referencia=referencia,
            ciudad=ciudad,
            estado=estado,
            es_principal=es_principal
        )
        nueva_direccion.save()  # Guardar en la base de datos

        # Agregar un mensaje de éxito
        print('¡La dirección ha sido agregada exitosamente!')
        return redirect('cuentaHome', user_id=usuario.id)

    # Si no es POST, mostrar el formulario
    return redirect('cuentaHome', user_id=usuario.id)  # Proporciona el user_id


#----------------------------------------------------------------------------------------------------------------#
# Vista administracion: home
@login_required
def homeAdmin(request):
    return render(request, 'administrador/inicioAdministrador.html', {'user': request.user})

# Vista administracion de clientes
def inicioClientesAdmin(request):
    return render(request, 'administrador/clientesAdmin/inicioClientesAdmin.html', {'user': request.user})

# Vista administracion: clientes: consulta
@login_required
def gestionar_clientes_admin(request):
    # Obtener todos los usuarios con rol de cliente
    clientes = Usuario.objects.filter(rol__nombre="cliente")  # Filtra los usuarios con rol 'cliente'
    
    # Renderizar la página con los clientes
    return render(request, 'administrador/clientesAdmin/gestionarClientesAdmin.html', {'clientes': clientes})

# Vista administracion: clientes: delete
@login_required
def eliminarClientesAdmin(request, cliente_id):
    # Obtener el cliente por id
    cliente = get_object_or_404(Usuario, id=cliente_id)

    if request.method == 'POST':
        # Cambiar el campo is_active a False
        cliente.is_active = False
        cliente.save()
        messages.success(request, f"El cliente {cliente.nombre} ha sido desactivado correctamente.")
        return redirect('gestionarClientesAdmin')  # Redirige a la página de gestión de clientes

    return render(request, 'administrador/clientesAdmin/eliminarClientesAdmin.html', {'cliente': cliente})

# Vista administracion: vendedores: home
def inicioVendedorAdmin(request):
    return render(request, 'administrador/vendedorAdmin/inicioVendedorAdmin.html', {'user': request.user})

# Vista administracion: vendedores: consulta
@login_required
def gestionarVendedorAdmin(request):
    # Obtener todos los usuarios con rol de cliente
    clientes = Usuario.objects.filter(rol__nombre="vendedor")  # Filtra los usuarios con rol 'cliente'
    
    # Renderizar la página con los clientes
    return render(request, 'administrador/vendedorAdmin/gestionarVendedorAdmin.html', {'clientes': clientes})

# Vista administracion: productos: home
def inicioProductosAdmin(request):
    return render(request, 'administrador/productosAdmin/inicioProductosAdmin.html', {'user': request.user})

# Vista administracion: productos: consulta
@login_required
def gestionarProductosAdmin(request):
        #Obtener todas las categorías
        productos = Producto.objects.all()

        #Renderizar la página con las categorías
        return render(request, 'administrador/productosAdmin/gestionarProductosAdmin.html', {'productos': productos})

# Vista administracion: pedidos: home
def inicioPedidosAdmin(request):
    return render(request, 'administrador/pedidosAdmin/inicioPedidosAdmin.html', {'user': request.user})

# Vista administracion: categorias: home
def inicioCategoriasAdmin(request):
    return render(request, 'administrador/categoriasAdmin/inicioCategoriasAdmin.html', {'user': request.user})

# Vista administracion: categorias: create
def crearCategoriaAdmin(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')

        # Crear la nueva categoría
        categoria = Categoria.objects.create(nombre=nombre, descripcion=descripcion)

        # Mensaje de éxito
        messages.success(request, f"La categoría '{categoria.nombre}' ha sido creada correctamente.")

        return redirect('inicioCategoriasAdmin')  # Redirigir a la página de gestión de categorías

    return render(request, 'administrador/categoriasAdmin/crearCategoriaAdmin.html')  # Mostrar el formulario

# Vista administracion: categoria: update
@login_required
def modificarCategoriasAdmin(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')

        # Actualizar la categoría
        categoria.nombre = nombre
        categoria.descripcion = descripcion
        categoria.save()

        # Mensaje de éxito
        messages.success(request, f"La categoría '{categoria.nombre}' ha sido actualizada correctamente.")

        return redirect('inicioCategoriasAdmin')  # Redirigir a la página de gestión de categorías

    return render(request, 'administrador/categoriasAdmin/modificarCategoriasAdmin.html', {'categoria': categoria})

# Vista administracion: categoria: consulta
def gestionarCategoriasAdmin(request):
    # Obtener todas las categorías con el conteo de productos relacionados
    categorias = Categoria.objects.annotate(productos_count=Count('producto'))

    # Renderizar la página con las categorías y el conteo de productos
    return render(request, 'administrador/categoriasAdmin/gestionarCategoriasAdmin.html', {'categorias': categorias})

# Vista administracion: categoria: drop
@login_required
def eliminarCategoriaAdmin(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)

    # Accede a los productos relacionados de la categoría
    productos = categoria.producto_set.all()  # Obtén todos los productos de esa categoría

    if productos.exists():
        # Realiza algo con los productos (por ejemplo, mostrar un mensaje)
        messages.error(request, f"La categoría {categoria.nombre} tiene productos asociados y no puede ser eliminada.")
        return redirect('gestionarCategoriasAdmin')

    if request.method == 'POST':
        categoria.delete()  # Eliminar la categoría
        messages.success(request, f"La categoría '{categoria.nombre}' ha sido eliminada correctamente.")
        return redirect('gestionarCategoriasAdmin')

    return render(request, 'administrador/categoriasAdmin/eliminarCategoriasAdmin.html', {'categoria': categoria})

#Vista administracion: pedidos: consulta
def inicioPedidosAdmin(request):
    # Obtener todos los pedidos que no estén cancelados
    pedidos = Pedido.objects.exclude(estatus='cancelado')

    print(f"Pedidos totales (sin cancelados): {pedidos.count()} encontrados.")

    # Renderizar la plantilla específica del administrador
    return render(request, 'administrador/pedidosAdmin/inicioPedidosAdmin.html', {
        'user': request.user,
        'pedidos': pedidos,  # Pasamos los pedidos al template
    })

#Vista administracion: pedidos: detalle
def detallePedidoAdmin(request, pedido_id):
    # Obtener el pedido específico o devolver un 404 si no existe
    pedido = get_object_or_404(Pedido, pk=pedido_id)

    # Obtener los detalles asociados a ese pedido
    detalles = DetallePedido.objects.filter(pedido=pedido)

    print(f"Detalles del Pedido {pedido.id}: {detalles.count()} productos encontrados.")

    # Renderizar la plantilla con la información del pedido y sus detalles
    return render(request, 'administrador/pedidosAdmin/detallePedidosAdmin.html', {
        'pedido': pedido,
        'detalles': detalles,
    })

# ---------------------------------------------------------------------------------------------------------------#
# Vista vendedor: home
@login_required
def homeVendedor(request):
    return render(request, 'vendedor/inicioVendedor.html', {'user': request.user})

# Vista vendedor: registro
def registro_vendedor_view(request):
    return render(request, 'registros/registroVendedor.html')

# Vista vendedor: registro endpoint
@api_view(['POST'])
def registrar_vendedor(request):
    # Asignar el rol "vendedor" directamente en la vista
    rol_vendedor = Rol.objects.get(nombre="vendedor")  # Obtener el rol "vendedor"
    
    # Crear una copia mutable del request.data y añadir el rol
    data = request.data.copy()  # Copiar los datos del request (mutable)
    data['rol'] = rol_vendedor.id  # Añadir el rol al diccionario
    
    # Crear el usuario con los datos proporcionados en el request
    serializer = UsuarioSerializer(data=data)
    
    if serializer.is_valid():
        serializer.save()
        return redirect('login')  # Redirige a la vista del login
    return Response(serializer.errors, status=400)

# Vista vendedor: productos: home
@login_required
def inicioProductosVendedor(request):
        # Verifica que tienes rol de vendedor
        if request.user.rol.nombre.lower() != 'vendedor':
            return HttpResponseForbidden("Acceso denegado: No tienes permisos para acceder a esta vista.")
        #Obtener todas las categorías
        productos = Producto.objects.filter(usuario=request.user)

        #Renderizar la página con las categorías
        return render(request, 'vendedor/productosVendedor/gestionarProductoVendedor.html', {'productos': productos})

# Vista vendedor: productos: create
@login_required
def crearProductoVendedor(request):
    # Verificar que el usuario tenga el rol de vendedor
    if request.user.rol.nombre.lower() != 'vendedor':
        # Usar reverse para obtener la URL del login
        login_url = reverse('login')
        return HttpResponseForbidden(f"""
            <h1>Acceso denegado</h1>
            <p>No tienes permisos para realizar esta acción.</p>
            <p><a href="{login_url}">Haz clic aquí para iniciar sesión</a></p>
        """)

    # Procesar el formulario cuando se envíe
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        costo = request.POST.get('costo')
        stock = request.POST.get('stock')
        categoria_id = request.POST.get('categoria')

        # Validar que los campos estén completos
        if not (nombre and descripcion and costo and stock and categoria_id):
            return render(request, 'vendedor/productosVendedor/crearProductoVendedor.html', {
                'categorias': Categoria.objects.all(),
                'error': 'Todos los campos son obligatorios.',
            })

        try:
            # Crear el producto
            categoria = Categoria.objects.get(id=categoria_id)
            Producto.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                costo=costo,
                stock=stock,
                categoria_id=categoria_id,
                usuario_id=request.user.id,
                is_active=True
            )
            return redirect('inicioProductosVendedor')  # Redirigir a una lista de productos (ajustar según necesidad)
        except Categoria.DoesNotExist:
            return render(request, 'productos/crearProductosVendedor.html', {
                'categorias': Categoria.objects.all(),
                'error': 'La categoría seleccionada no existe.',
            })

    # Si el método es GET, renderizar el formulario
    return render(request, 'vendedor/productosVendedor/crearProductoVendedor.html', {
        'categorias': Categoria.objects.all(),
    })

# Vista vendedor: productos: modificar
@login_required
def modificarProductoVendedor(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        stock = request.POST.get('stock')
        costo = request.POST.get('costo')

        # Actualizar la categoría
        producto.nombre = nombre
        producto.descripcion = descripcion
        producto.stock = stock
        producto.costo = costo
        producto.save()

        # Mensaje de éxito
        messages.success(request, f"El producto '{producto.nombre}' ha sido actualizada correctamente.")

        return redirect('inicioProductosVendedor')  # Redirigir a la página de gestión de categorías

    return render(request, 'vendedor/productosVendedor/modificarProductoVendedor.html', {'producto': producto})

# Vista Vendedor: Productos: drop
@login_required
def eliminarProductoVendedor(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        # Marcar el producto como inactivo
        producto.is_active = False
        producto.save()
        messages.success(request, f"El producto '{producto.nombre}' ha sido marcado como inactivo.")
        return redirect('inicioProductosVendedor')

    return render(request, 'vendedor/productosVendedor/eliminarProductoVendedor.html', {'producto': producto})


# Vista vendedor: pedidos: home
def inicioPedidosVendedor(request):
    return render(request, 'vendedor/pedidosVendedor/inicioPedidosVendedor.html', {'user': request.user})

@login_required
def gestionarProductoVendedor(request):
    productos = Producto.objects.all()  # Obtén todos los productos
    return render(request, 'vendedor/productosVendedor/gestionarProductoVendedor.html', {'productos': productos})
#----------------------------------------------------------------------------------------------------------------#
#Vista Clientes: home
@login_required
def homeCliente(request):
    # Obtener todos los productos activos y categorías
    productos = Producto.objects.filter(is_active=True)  # Filtrar productos activos
    categorias = Categoria.objects.all()

    # Filtrar productos según la búsqueda
    query = request.GET.get('search', '')
    categoria_id = request.GET.get('categoria', '')

    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query)
        )
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    return render(request, 'cliente/inicioCliente.html', {
        'productos': productos,
        'categorias': categorias,
    })
# Vista Clientes: registro
def registro_clientes_view(request):
    return render(request, 'registros/registroCliente.html')

# Vista Clientes: registro endpoint
@api_view(['POST'])
def registrar_cliente(request):
    # Asignar el rol "cliente" directamente en la vista
    rol_cliente = Rol.objects.get(nombre="cliente")  # Obtener el rol "cliente"
    
    # Crear una copia mutable del request.data y añadir el rol
    data = request.data.copy()  # Copiar los datos del request (mutable)
    data['rol'] = rol_cliente.id  # Añadir el rol al diccionario
    
    # Crear el usuario con los datos proporcionados en el request
    serializer = UsuarioSerializer(data=data)
    
    if serializer.is_valid():
        serializer.save()
        return redirect('login')  # Redirige a la vista del login
    return Response(serializer.errors, status=400)
    
# Vista Clientes: pedidos: home
def ClientePedidosHome(request):
    return render(request, 'cliente/pedidosCliente/inicioPedidosCliente.html', {'user': request.user})

#----------------------------------------------------------------------------------------------------------------#
# Vista Carrito: Home
@login_required
def agregar_a_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)

    # Busca si el producto ya está en el carrito
    carrito_item, item_created = CarritoItems.objects.get_or_create(
        carrito=carrito,
        producto=producto
    )
    if not item_created:
        # Incrementa la cantidad si el producto ya existe
        carrito_item.cantidad += 1
        carrito_item.save()

    return redirect('homeCliente')  # Cambia 'productos' por el nombre del URL de tus productos.
 # Vista Carrito: seguir comprando

# Vista Carrito: seguir comprando
def seguir_comprando(request):
    return redirect('homeCliente')

# Vista carrito: ver carrito
def ver_carrito(request):
    try:
        # Intentamos obtener el carrito del usuario
        carrito = Carrito.objects.get(usuario=request.user)
        cart_items = carrito.items.all()

        # Verificamos si el carrito tiene elementos
        if cart_items.exists():
            total_price = carrito.get_total_price()
        else:
            total_price = 0  # Si no hay productos, el total es 0

    except Carrito.DoesNotExist:
        # Si el carrito no existe, mostramos un mensaje y asignamos un carrito vacío
        carrito = None
        cart_items = []
        total_price = 0
        messages.info(request, "Tu carrito está vacío.")
    
    # Renderizamos la página con el carrito (vacío o con productos)
    return render(request, 'carrito/carrito.html', {
        'carrito': carrito,
        'cart_items': cart_items,
        'total_price': total_price
    })

# Vista Carrito: Producto: drop
def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(CarritoItems, id=item_id)
    item.delete()
    return redirect('carrito')

# Vista Carrito: Producto: update
def actualizar_cantidad(request, item_id):
    item = get_object_or_404(CarritoItems, id=item_id)
    
    if request.method == "POST":
        cantidad = request.POST.get('cantidad')
        
        try:
            cantidad = int(cantidad)
            if cantidad > 0:
                item.cantidad = cantidad
                item.save()
            else:
                item.delete()  # Si la cantidad es 0 o negativa, eliminamos el ítem del carrito
        except ValueError:
            pass  # Si la cantidad no es un número válido, no hacemos nada.
        
        return redirect('carrito')  # Redirigimos al carrito con la cantidad actualizada

    return redirect('carrito')

#----------------------------------------------------------------------------------------------------------------#
# Vista Pedido: Cliente: Consulta
def verPedido(request, user_id):
    # Obtener el usuario con el ID proporcionado
    usuario = get_object_or_404(Usuario, id=user_id)

    print(f"Usuario: {usuario.usuario} (ID: {usuario.id}) (Rol: {usuario.rol})")

    detalles_pedidos = []

    # Asignar un valor predeterminado para template_name
    template_name = 'pedidos/basePedidos.html'  # Valor predeterminado para el template

    # Determinar el template según el rol del usuario
    rol_normalizado = usuario.rol.nombre.strip().lower()

    if rol_normalizado == 'cliente':
        pedidos = Pedido.objects.filter(usuario=usuario.id).exclude(estatus='cancelado')
        print(f"Pedidos del Cliente: {pedidos.count()} encontrados.")
        for pedido in pedidos:
            detalles_pedido_cliente = pedido.detalles.all()
            if detalles_pedido_cliente.exists():
                detalles_pedidos.append(detalles_pedido_cliente)
                print(f"Pedido {pedido.id} tiene {detalles_pedido_cliente.count()} productos.")
        template_name = 'pedidos/pedidosCliente/verPedido_Cliente.html'

    elif rol_normalizado == 'administrador':
        pedidos = Pedido.objects.exclude(estatus='cancelado')
        template_name = 'pedidos/pedidosAdministracion/verPedido_Administrador.html'

    elif rol_normalizado == 'vendedor':
        pedidos = Pedido.objects.filter(detalles__producto__usuario=usuario).exclude(estatus='cancelado').distinct()
        print(f"Pedidos del Vendedor: {pedidos.count()} encontrados.")
        for pedido in pedidos:
            detalles_pedido_vendedor = pedido.detalles.filter(producto__usuario=usuario)
            if detalles_pedido_vendedor.exists():
                detalles_pedidos.append(detalles_pedido_vendedor)
                print(f"Pedido {pedido.id} tiene {detalles_pedido_vendedor.count()} productos del vendedor.")
        template_name = 'pedidos/pedidosVendedor/verPedido_Vendedor.html'

    return render(request, template_name, {
        'usuario': usuario,
        'pedidos': pedidos,
        'detalles_pedidos': detalles_pedidos,
    })




# Vista Pedido: Cliente: Detalles
def ver_detalles_pedido(request, pedido_id, user_id):
    # Obtener el pedido usando el ID
    pedido = get_object_or_404(Pedido, id=pedido_id)
    
    # Obtener el usuario con el ID proporcionado
    usuario = get_object_or_404(Usuario, id=user_id)
    
    # Obtener los detalles de este pedido
    detalles = pedido.detalles.all()

    print(f"Usuario rol original: {usuario.rol}")

    # Normalizar el rol
    rol_normalizado = usuario.rol.nombre.strip().lower()
    print(f"Usuario rol normalizado: {rol_normalizado}")

    if rol_normalizado == 'cliente':
        template_name = 'pedidos/pedidosCliente/verDetallePedido_Cliente.html'
    elif rol_normalizado == 'administrador':
        template_name = 'pedidos/pedidosAdministracion/verDetallePedido_Administrador.html'
    elif rol_normalizado == 'vendedor':
        template_name = 'pedidos/pedidosVendedor/verDetallePedido_Vendedor.html'
    else:
        print("Rol no encontrado.")
        template_name = 'pedidos/baseDetallePedido.html'

    print(f"Usando template: {template_name}")
    return render(request, template_name, {
        'usuario': usuario,
        'pedido': pedido,
        'detalles': detalles,
    })


# Vista Pedido: Cliente: Cancelar
def cancelar_pedido(request, pedido_id):
    # Obtener el pedido por ID
    pedido = get_object_or_404(Pedido, id=pedido_id)

    # Cambiar el estatus a 'cancelado'
    if pedido.estatus.lower() != 'cancelado':# Verifica que no esté ya cancelado
        pedido.estatus = 'Cancelado'
        pedido.save()
        messages.success(request, "El pedido ha sido cancelado exitosamente.")
    else:
        messages.warning(request, "Este pedido ya ha sido cancelado.")

    # Obtener el user_id del usuario asociado al pedido
    user_id = pedido.usuario.id

    # Redirigir a la página de verPedidoCliente
    return redirect('verPedido', user_id=user_id)

# Visto Pedido: Crear Pedido
def crear_pedido(request, user_id):
    print("Entrando en la vista crear_pedido...")  # Debugging
    usuario = get_object_or_404(Usuario, id=user_id)
    carrito = Carrito.objects.get(usuario=request.user)
    carrito_items = carrito.items.all()
    #print("Carrito items:", carrito_items)  # Debugging
    carrito_total = sum(item.get_total_price() for item in carrito_items)

    # Verificar si el carrito está vacío
    if not carrito_items:
        print("Carrito vacío.")  # Debugging
        messages.error(request, 'Tu carrito está vacío. No puedes proceder con la compra.')
        return redirect('homeCliente')  # Redirigir a la página principal

    print("Carrito tiene productos. Renderizando confirmarPedido.html...")  # Debugging
    # Mostrar la página de confirmación
    return render(request, 'pedidos/confirmarPedido.html', {'usuario': usuario, 'carrito_items': carrito_items, 'direcciones': usuario.direccion_set.all(), 'carrito_total': carrito_total})


# Vista Pedido: Confirmar Pedido
def confirmar_pedido(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)
    carrito = Carrito.objects.get(usuario=request.user)
    carrito_items = carrito.items.all()

    if request.method == "POST":
        direccion_id = request.POST.get("direccion")
        direccion = get_object_or_404(usuario.direccion_set, id=direccion_id)

        # Crear el pedido con la dirección seleccionada
        pedido = Pedido.objects.create(
            usuario=request.user,
            fecha_pedido=timezone.now(),
            fecha_entrega=None,
            estatus='pendiente',
            direccion=direccion
        )

        # Crear los detalles del pedido a partir de los elementos en el carrito
        DetallePedido.crear_detalles_pedido(carrito_items, pedido)

        # Limpiar el carrito después de la compra
        carrito.clear_cart()

        # Establecer una fecha de entrega
        fecha_entrega = timezone.now() + timezone.timedelta(days=7)
        pedido.fecha_entrega = fecha_entrega
        pedido.save()

        messages.success(request, "Pedido confirmado con éxito.")
        return redirect('verPedido', user_id=usuario.id)

    # Si el método no es POST, mostrar la página de confirmación
    return render(request, 'pedidos/confirmarPedido.html', {
        'usuario': usuario,
        'carrito_items': carrito_items
    })

def prueba_confirmar_pedido(request):
    return render(request, 'pedidos/confirmarPedido.html')
