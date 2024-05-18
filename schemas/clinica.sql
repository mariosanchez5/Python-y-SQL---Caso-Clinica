CREATE TABLE habitaciones (
    id_habitacion serial PRIMARY KEY
);


CREATE TABLE camas (
    id_cama serial PRIMARY KEY,
    disponible BOOLEAN,
    habitaciones_id INT,
    FOREIGN KEY (habitaciones_id) REFERENCES habitaciones(id_habitacion)
);


CREATE TABLE medicos (
    id_medico serial PRIMARY KEY,
    nombre VARCHAR(50),
	apellido VARCHAR(50),
    rut INT
);


CREATE TABLE pacientes (
    id_paciente serial PRIMARY KEY,
    nombre VARCHAR(50),
	apellido VARCHAR(50),
	rut VARCHAR(50),
    medicos_id INT,
    camas_id INT,
    FOREIGN KEY (medicos_id) REFERENCES medicos(id_medico),
    FOREIGN KEY (camas_id) REFERENCES camas(id_cama)
);



CREATE TABLE examenes (
    id_examen serial PRIMARY KEY,
    nombre VARCHAR(100),
    resultado VARCHAR(100),
    medicos_id INT,
    pacientes_id INT,
    FOREIGN KEY (medicos_id) REFERENCES medicos(id_medico),
    FOREIGN KEY (pacientes_id) REFERENCES pacientes(id_paciente),
    fecha DATE
);


CREATE TABLE diagnosticos (
    id_diagnostico serial PRIMARY KEY,
    pacientes_id INT,
    medicos_id INT,
    FOREIGN KEY (pacientes_id) REFERENCES pacientes(id_paciente),
    FOREIGN KEY (medicos_id) REFERENCES medicos(id_medico),
    enfermedad VARCHAR(100)
);

