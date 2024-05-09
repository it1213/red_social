<?php
// Establecer la conexión con la base de datos
$conexion = new mysqli("localhost", "usuario", "contraseña", "red_social");

// Verificar la conexión
if ($conexion->connect_error) {
    die("Error de conexión: " . $conexion->connect_error);
}

// Obtener los datos del formulario
$email = $_POST['email'];
$password = $_POST['password'];

// Consulta SQL para verificar las credenciales
$sql = "SELECT * FROM usuarios WHERE email = '$email' AND password = '$password'";
$resultado = $conexion->query($sql);

// Verificar si se encontró un usuario con las credenciales proporcionadas
if ($resultado->num_rows > 0) {
    // Usuario autenticado, redirigir a index.html
    header("Location: index.html");
} else {
    // Mostrar mensaje de error si las credenciales son incorrectas
    echo "Correo electrónico o contraseña incorrectos";
}

// Cerrar la conexión a la base de datos
$conexion->close();
