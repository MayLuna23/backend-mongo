// Script de inicialización de MongoDB
// Este script se ejecuta automáticamente al crear el contenedor

// Cambiar a la base de datos numbers_db
db = db.getSiblingDB('numbers_db');

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