from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from models import Product, get_db
from schemas import product_schema, products_schema

api_bp = Blueprint('api', __name__)
db = next(get_db())

@api_bp.route('/products', methods=['GET'])
def get_products():
    try:
        limit = request.args.get('limit', default=10, type=int)
        products = db.query(Product).limit(limit).all()
        return jsonify(products_schema.dump(products))
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@api_bp.route('/products/search', methods=['GET'])
def search_products():
    try:
        search = request.args.get('q', '')
        products = db.query(Product).filter(
            Product.nombre_producto.ilike(f'%{search}%')  # Changed to match your column name
        ).all()
        return jsonify(products_schema.dump(products))
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@api_bp.route('/products/<name>', methods=['GET'])
def get_product(name):
    try:
        product = db.query(Product).filter(Product.nombre_producto == name).first()  # Changed to match your column name
        if not product:
            return jsonify({'message': 'Product not found'}), 404
        return jsonify(product_schema.dump(product))
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@api_bp.route('/products/<name>', methods=['PATCH'])
def update_product(name):
    try:
        data = request.get_json()
        if 'stock' not in data or 'bodega' not in data:
            return jsonify({'message': 'Stock and bodega are required'}), 400
        
        product = db.query(Product).filter(Product.nombre_producto == name).first()  # Changed to match your column name
        if not product:
            return jsonify({'message': 'Product not found'}), 404
        
        product.stock = data['stock']
        product.bodega = data['bodega']
        db.commit()
        return jsonify({'message': 'Product updated successfully'})
    except Exception as e:
        db.rollback()
        return jsonify({'message': str(e)}), 500

@api_bp.route('/products', methods=['POST'])
def add_product():
    try:
        data = request.get_json()
        product = Product(
            id_producto=data['id_producto'],
            nombre_producto=data['nombre_producto'],  # Changed to match your column name
            stock=data['stock'],
            bodega=data['bodega']
        )
        db.add(product)
        db.commit()
        return jsonify({'message': 'Product added successfully'}), 201
    except IntegrityError:
        db.rollback()
        return jsonify({'message': 'Product name already exists'}), 409
    except KeyError:
        return jsonify({'message': 'Missing required fields'}), 400
    except Exception as e:
        db.rollback()
        return jsonify({'message': str(e)}), 500