# tests/conftest.py
import os, sys
# garante que a raiz do projeto esteja no sys.path para TODOS os testes
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
