CREATE TABLE habitaciones (
    id_habitacion VARCHAR(50) PRIMARY KEY,
    camas_ids INT[]
);


CREATE TABLE camas (
    id_cama INT PRIMARY KEY,
    disponible BOOLEAN,
    habitaciones_id VARCHAR(50),
    FOREIGN KEY (habitaciones_id) REFERENCES habitaciones(id_habitacion)
);


CREATE TABLE medicos (
    rut INT PRIMARY KEY,
    nombre VARCHAR(50),
	apellido VARCHAR(50)
);


CREATE TABLE pacientes (
    rut INT PRIMARY KEY,
    nombre VARCHAR(50),
	apellido VARCHAR(50),
    medicos_id INT,
    camas_id INT,
    FOREIGN KEY (medicos_id) REFERENCES medicos(rut),
    FOREIGN KEY (camas_id) REFERENCES camas(id_cama)
);



CREATE TABLE examenes (
    id_examen INT PRIMARY KEY,
    nombre VARCHAR(100),
    resultado VARCHAR(100),
    medicos_id INT,
    pacientes_id INT,
    FOREIGN KEY (medicos_id) REFERENCES medicos(rut),
    FOREIGN KEY (pacientes_id) REFERENCES pacientes(rut),
    fecha DATE
);


CREATE TABLE diagnosticos (
    id_diagnostico INT PRIMARY KEY,
    pacientes_id INT,
    medicos_id INT,
    FOREIGN KEY (pacientes_id) REFERENCES pacientes(rut),
    FOREIGN KEY (medicos_id) REFERENCES medicos(rut),
    enfermedad VARCHAR(100),
    examenes_id INT[]
);

