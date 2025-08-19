
CREATE TABLE IF NOT EXISTS branches (
    branch_id VARCHAR(36) PRIMARY KEY,
    branch_name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id VARCHAR(36) PRIMARY KEY, 
    branch_id VARCHAR(36) NOT NULL,        
    date DATE NOT NULL,
    time TIME NOT NULL,
    total DECIMAL(10, 2),                 
    trans_type VARCHAR(50),
    CONSTRAINT fk_branch
        FOREIGN KEY (branch_id)
        REFERENCES branches(branch_id)
        ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS products (
    product_id VARCHAR(36) PRIMARY KEY,   
    product_name VARCHAR(50),
    price DECIMAL(10, 2) NOT NULL
);