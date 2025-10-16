// Script de inicialización de MongoDB
// Este script se ejecuta automáticamente al crear el contenedor

print('==================================================');
print('Iniciando configuración de la base de datos...');
print('==================================================');

// Cambiar a la base de datos numbers_db
db = db.getSiblingDB('numbers_db');

// // Crear colección de usuarios
// print('Creando colección: users');
// db.createCollection('users', {
//     validator: {
//         $jsonSchema: {
//             bsonType: "object",
//             required: ["username", "password", "created_at"],
//             properties: {
//                 username: {
//                     bsonType: "string",
//                     description: "Nombre de usuario - requerido"
//                 },
//                 password: {
//                     bsonType: "string",
//                     description: "Contraseña hasheada - requerida"
//                 },
//                 created_at: {
//                     bsonType: "string",
//                     description: "Fecha de creación - requerida"
//                 }
//             }
//         }
//     }
// });

// Crear colección de números
print('Creando colección: numbers');
db.createCollection('numbers', {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["username", "value", "created_at"],
            properties: {
                username: {
                    bsonType: "string",
                    description: "Nombre del usuario - requerido"
                },
                value: {
                    bsonType: "int",
                    minimum: 1,
                    description: "Valor numérico mayor a 0 - requerido"
                },
                created_at: {
                    bsonType: "string",
                    description: "Fecha de creación - requerida"
                }
            }
        }
    }
});

// // Insertar usuario predefinido (admin)
// print('Insertando usuario predefinido: admin');
// db.users.insertOne({
//     username: "admin",
//     password: "1234",
//     created_at: new Date().toISOString(),
// });

// // Crear índices para mejorar el rendimiento
// print('Creando índices...');

// // Índice único en username para usuarios
// db.users.createIndex({ "username": 1 }, { unique: true });

// // Índices para la colección numbers
// db.numbers.createIndex({ "username": 1 });
// db.numbers.createIndex({ "created_at": -1 });
// db.numbers.createIndex({ "username": 1, "created_at": -1 });

// // Verificar las colecciones creadas
// print('==================================================');
// print('Colecciones en la base de datos:');
// db.getCollectionNames().forEach(function(collection) {
//     print('  - ' + collection);
// });

// // Verificar el usuario insertado
// print('==================================================');
// print('Usuario creado:');
// var user = db.users.findOne({ username: "admin" });
// if (user) {
//     print('  Username: ' + user.username);
//     print('  Created: ' + user.created_at);
// } else {
//     print('  ERROR: No se pudo crear el usuario');
// }

// print('==================================================');
// print('Configuración completada exitosamente!');
// print('==================================================');