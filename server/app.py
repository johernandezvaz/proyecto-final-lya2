from flask import Flask, request, jsonify
from flask_cors import CORS
from compiler.lexer import lex
from compiler.parser import Parser
from compiler.interpreter import Interpreter
from compiler.automata import AutomataVisualizer
from compiler.semantic_translator import SemanticTranslator
from compiler.code_generator import CodeGenerator

app = Flask(__name__)
CORS(app)

@app.route('/api/analyze/lexer', methods=['POST'])
def analyze_lexer():
    try:
        code = request.json.get('code', '')
        tokens = lex(code)
        return jsonify({'tokens': tokens})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/analyze/parser', methods=['POST'])
def analyze_parser():
    try:
        code = request.json.get('code', '')
        tokens = lex(code)
        parser = Parser(tokens)
        ast = parser.parse()
        return jsonify({'ast': ast.to_dict()})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/analyze/semantic', methods=['POST'])
def analyze_semantic():
    try:
        code = request.json.get('code', '')
        tokens = lex(code)
        parser = Parser(tokens)
        ast = parser.parse()
        
        translator = SemanticTranslator()
        ir_code = translator.translate(ast.to_dict())
        
        code_generator = CodeGenerator()
        target_code = code_generator.generate_code(ir_code)
        
        return jsonify({
            'intermediate_code': ir_code,
            'target_code': target_code
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/run', methods=['POST'])
def run_program():
    try:
        code = request.json.get('code', '')
        tokens = lex(code)
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        output = interpreter.evaluate(ast.to_dict())
        return jsonify({'output': output})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/language/theory', methods=['GET'])
def get_language_theory():
    try:
        visualizer = AutomataVisualizer()
        automaton = visualizer.create_lexer_automaton()
        grammar = visualizer.get_grammar()
        token_types = visualizer.get_token_types()
        
        return jsonify({
            'automaton': automaton.source,
            'grammar': grammar,
            'token_types': token_types
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)