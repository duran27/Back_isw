from marshmallow import Schema, fields, validate

class ProductSchema(Schema):
    id_producto = fields.Int(required=True)  # Changed to match your column name
    nombre_producto = fields.Str(required=True)  # Changed to match your column name
    stock = fields.Int(required=True)
    bodega = fields.Int(required=True, validate=validate.Range(min=1, max=3))  # Changed to match your column name

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)