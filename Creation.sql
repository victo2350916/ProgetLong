# Création de la base de données
DROP DATABASE IF EXISTS projet_long;
CREATE DATABASE projet_long;
USE projet_long;

# Création de la table clients
CREATE TABLE clients(
	id INT AUTO_INCREMENT,
    nom VARCHAR(50),
    numero_telephone VARCHAR(50),
    adresse VARCHAR(255),
    PRIMARY KEY (id)
);

# Création de la table commandes
CREATE TABLE commandes(
	id INT AUTO_INCREMENT,
    client_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

# Création de la table commande_attente
CREATE TABLE commande_attente(
	id 	INT AUTO_INCREMENT,
    commande_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY (commande_id) REFERENCES commandes(id)
);

# Création de la table croutes
CREATE TABLE croutes(
	id INT AUTO_INCREMENT,
    type VARCHAR(50),
    PRIMARY KEY (id)
);

# Création de la table sauces
CREATE TABLE sauces(
	id INT AUTO_INCREMENT,
    type VARCHAR(50),
    PRIMARY KEY (id)
);

# Création de la table pizza
CREATE TABLE pizza(
	id INT AUTO_INCREMENT,
    commande_id INT,
    croute_id INT,
    sauce_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY (commande_id) REFERENCES commandes(id),
    FOREIGN KEY (croute_id) REFERENCES croutes(id),
    FOREIGN KEY (sauce_id) REFERENCES sauces(id)
);

# Création de la table garnitures
CREATE TABLE garnitures(
	id INT AUTO_INCREMENT,
    type VARCHAR(255),
    PRIMARY KEY (id)
);

# Création de la table pizza garniture
CREATE TABLE pizza_garniture(
	id INT AUTO_INCREMENT,
	pizza_id INT,
    garniture_id INT,
	PRIMARY KEY (id),
    FOREIGN KEY (pizza_id) REFERENCES pizza(id),
    FOREIGN KEY (garniture_id) REFERENCES garnitures(id)
);

# Création du déclencheur pour les commandes en attente
DELIMITER $$

CREATE TRIGGER commande_attente
AFTER INSERT ON commandes
FOR EACH ROW
BEGIN
	INSERT INTO commande_attente (commande_id)
		VALUES (NEW.id);
END$$

DELIMITER ;