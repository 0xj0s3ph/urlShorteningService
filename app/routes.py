from flask import Blueprint, jsonify, request
from .models import db, URL
import string
import random


def generate_short_code(length=6):
    """Generate a random short code for URLs"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Create a Blueprint
main = Blueprint('main', __name__)

# Home route
@main.route('/')
def home():
    return jsonify({'message': 'Welcome to the home page!'})

@main.route('/urls/',methods=['POST'])
def create_url():
    # Check if Content-Type is application/json
    if not request.is_json:
        return jsonify({
            'error': 'Content-Type must be application/json'
        }), 415

    try:
        # Get JSON data from request
        data = request.get_json()

        if not data or 'url' not in data:
            return jsonify({
                'error': 'Missing required parameter: url'
            }), 400

        original_url = data['url']

        # Generate unique short code
        while True:
            short_code = generate_short_code()
            if not URL.query.filter_by(short_code=short_code).first():
                break

        # Create new URL object
        url_entry = URL(
            original_url=original_url,
            short_code=short_code
        )

        db.session.add(url_entry)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'data': url_entry.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to create URL',
            'message': str(e)
        }), 500


@main.route('/urls/',methods=['GET'])
def get_urls():
    try:
        urls = URL.query.all()
        return jsonify({
            'status': 'success',
            'data': [url.to_dict() for url in urls]
        })
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve URLs',
            'message': str(e)
        }), 500

@main.route('/urls/<short_code>',methods=['GET'])
def get_url(short_code):
    url_entry = URL.query.filter_by(short_code=short_code).first()
    if url_entry:
        url_entry.accessed_times += 1
        db.session.commit()
        return jsonify({
            'status': 'success',
            'data': url_entry.to_dict()
        })
    return jsonify({'error': 'URL not found'}), 404


@main.route('/urls/<url_id>', methods=['PATCH'])
def update_url(url_id):
    if not request.is_json:
        return jsonify({
            'error': 'Content-Type must be application/json'
        }), 415

    try:
        # Get URL entry by ID
        url_entry = URL.query.get(url_id)
        if not url_entry:
            return jsonify({'error': 'URL not found'}), 404

        # Get JSON data from request
        data = request.get_json()

        # Check if any valid fields are provided
        valid_fields = {'original_url'}
        update_fields = set(data.keys()) & valid_fields

        if not update_fields:
            return jsonify({
                'error': 'No valid fields to update provided',
                'valid_fields': list(valid_fields)
            }), 400

        # Update fields
        if 'original_url' in data:
            url_entry.original_url = data['original_url']

        db.session.commit()

        return jsonify({
            'status': 'success',
            'data': url_entry.to_dict()
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to update URL',
            'message': str(e)
        }), 500

@main.route('/urls/<url_id>', methods=['DELETE'])
def delete_url(url_id):
    try:
        # Get URL entry by ID
        url_entry = URL.query.get(url_id) #url_id: primary key of the record
        if not url_entry:
            return jsonify({'error': 'URL not found'}), 404

        # Delete the URL entry
        db.session.delete(url_entry)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': f'URL with ID {url_id} has been deleted'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to delete URL',
            'message': str(e)
        }), 500
