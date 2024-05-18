CREATE TABLE habitaciones (
    id_habitacion INT PRIMARY KEY,
);


CREATE TABLE cama (
    id_cama INT PRIMARY KEY,
    disponible BOOLEAN,
    FOREIGN KEY (habitaciones_id) REFERENCES habitaciones(id_habitacion)
);


CREATE TABLE medicos (
    id_medico INT PRIMARY KEY,
    nombre VARCHAR(50),
	apellido VARCHAR(50),
    rut INT
);


CREATE TABLE pacientes (
    id_paciente INT PRIMARY KEY,
    nombre VARCHAR(50),
	apellido VARCHAR(50),
	rut VARCHAR(50),
    FOREIGN KEY (medicos_id) REFERENCES medicos(id_medico),
    FOREIGN KEY (camas_id) REFERENCES camas(id_cama)
);



CREATE TABLE examenes (
    id_examen INT PRIMARY KEY,
    nombre VARCHAR(100),
    resultado VARCHAR(100),
    FOREIGN KEY (medicos_id) REFERENCES medicos(id_medico),
    FOREIGN KEY (pacientes_id) REFERENCES pacientes(id_paciente),
    fecha DATE
);


CREATE TABLE diagnosticos (
    id_diagnostico INT PRIMARY KEY,
    FOREIGN KEY (pacientes_id) REFERENCES pacientes(id_paciente),
    FOREIGN KEY (medicos_id) REFERENCES medicos(id_medico),
    enfermedad VARCHAR(100)
);

