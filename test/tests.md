curl -i -X POST http://127.0.0.1:5000/registro \
  -H "Content-Type: application/json" \
  -d '{"usuario":"gabriel","contraseña":"1234"}'

curl -i -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"usuario":"gabriel","contraseña":"1234"}'

curl -i -u gabriel:1234 http://127.0.0.1:5000/tareas
