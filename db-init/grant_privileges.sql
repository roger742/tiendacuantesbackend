-- Revocar todos los privilegios primero (seguridad)
REVOKE ALL PRIVILEGES, GRANT OPTION FROM 'tienda'@'%';

-- Otorgar privilegios personalizados al usuario 'tienda'
GRANT ALL PRIVILEGES ON tiendavirtual.* TO 'tienda'@'%' WITH GRANT OPTION;
REVOKE DROP ON tiendavirtual.* FROM 'tienda'@'%';

-- Aplicar cambios
FLUSH PRIVILEGES;