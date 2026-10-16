// ==========================================
// MÓDULO 1: USUARIOS, ROLES Y AUTENTICACIÓN
// ==========================================

Table rol {
  id integer [primary key, increment]
  nombre_rol varchar [not null]
}

Table usuario {
  id integer [primary key, increment]
  empleado_id integer [not null, unique]
  correo varchar [unique, not null]
  contrasena_hash varchar [not null]
  rol_id integer [not null]
}

// ==========================================
// MÓDULO 2: GESTIÓN DE PERSONAL Y HORARIOS
// ==========================================

Table cargo {
  id integer [primary key, increment]
  nombre_cargo varchar [not null]
}

Table horario {
  id integer [primary key, increment]
  nombre_horario varchar [not null]
  hora_entrada_teorica time [not null]
  hora_salida_teorica time [not null]
}

Table empleado {
  id integer [primary key, increment]
  nombre varchar [not null]
  apellido varchar [not null]
  cedula varchar [unique, not null]
  id_empleado_biometrico integer [unique, note: 'ID numérico que arroja el reloj ZKTeco']
  cargo_id integer [not null]
  horario_id integer [not null]
}

// ==========================================
// MÓDULO 3: MOTOR BIOMÉTRICO Y ASISTENCIA
// ==========================================

Table marcaje_crudo {
  id integer [primary key, increment]
  id_empleado_biometrico integer [not null]
  fecha_hora_marcaje timestamp [not null]
  tipo_marcaje varchar [note: 'entrada o salida']
}

Table estatus_asistencia {
  id integer [primary key, increment]
  nombre_estatus varchar [not null]
}

Table asistencia_diaria {
  id integer [primary key, increment]
  empleado_id integer [not null]
  fecha date [not null]
  hora_entrada time
  hora_salida time
  minutos_tarde integer
  estatus_id integer [not null]
  modificado_manualmente boolean [default: false]
}

// ==========================================
// MÓDULO 4: PERMISOS Y JUSTIFICATIVOS
// ==========================================

Table tipo_ausencia {
  id integer [primary key, increment]
  nombre_tipo varchar [not null]
}

Table ausencia {
  id integer [primary key, increment]
  empleado_id integer [not null]
  tipo_ausencia_id integer [not null]
  fecha_inicio date [not null]
  fecha_fin date [not null]
  descripcion text
  archivo_pdf_ruta varchar
  estado_aprobacion varchar [default: 'Pendiente']
  aprobado_por_usuario_id integer [note: 'ID del Admin que aprobó']
  fecha_solicitud timestamp
}


// ==========================================
// RELACIONES (Llaves foráneas)
// ==========================================

// Relaciones Módulo 1
Ref: usuario.rol_id > rol.id
Ref: usuario.empleado_id - empleado.id // Relación 1 a 1 (Un empleado tiene un usuario)

// Relaciones Módulo 2
Ref: empleado.cargo_id > cargo.id
Ref: empleado.horario_id > horario.id

// Relaciones Módulo 3
// El reloj se comunica a través del ID del biométrico, no del ID de la base de datos
Ref: marcaje_crudo.id_empleado_biometrico > empleado.id_empleado_biometrico
Ref: asistencia_diaria.empleado_id > empleado.id
Ref: asistencia_diaria.estatus_id > estatus_asistencia.id

// Relaciones Módulo 4
Ref: ausencia.empleado_id > empleado.id
Ref: ausencia.tipo_ausencia_id > tipo_ausencia.id
Ref: ausencia.aprobado_por_usuario_id > usuario.id


// ==========================================
// DATOS DE EJEMPLO (Para visualizar mejor)
// ==========================================

Records rol(id, nombre_rol) {
  1, 'Superadmin'
  2, 'Admin'
  3, 'User'
}

Records cargo(id, nombre_cargo) {
  1, 'Administrativo'
  2, 'Docente'
  3, 'Obrero'
}

Records horario(id, nombre_horario, hora_entrada_teorica, hora_salida_teorica) {
  1, 'Mañana', '07:00:00', '13:00:00'
  2, 'Tarde', '13:00:00', '18:00:00'
  3, 'Mixto', '08:00:00', '16:00:00'
}

Records estatus_asistencia(id, nombre_estatus) {
  1, 'A Tiempo'
  2, 'Retrasado'
  3, 'Inasistente'
}

Records tipo_ausencia(id, nombre_tipo) {
  1, 'Justificativo'
  2, 'Permiso'
  3, 'Reposo'
  4, 'Falta Injustificada'
}