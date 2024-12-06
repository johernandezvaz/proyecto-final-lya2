import  { useState, useEffect } from 'react';
import CodeMirror from '@uiw/react-codemirror';
import { python } from '@codemirror/lang-python';
import { oneDark } from '@codemirror/theme-one-dark';
import { Panel, PanelGroup, PanelResizeHandle } from 'react-resizable-panels';
import { FaPlay, FaCode, FaTree, FaBook, FaCogs } from 'react-icons/fa';
import AutomataVisualizer from './components/AutomataVisualizer';

const defaultCode = `main {
  nombre x = 10;
  crêpe y = 3.14;
  afficher("Bonjour!");
  
  macaron (x > 5) {
      afficher(x);
  } autre {
      afficher(y);
  }
  
  tour_eiffel (x > 0) {
      afficher(x);
      x = x - 1;
  }
}`;

function App() {
const [code, setCode] = useState(defaultCode);
const [output, setOutput] = useState('');
const [activeTab, setActiveTab] = useState('lexer');
const [languageTheory, setLanguageTheory] = useState(null);
const [lastRunTab, setLastRunTab] = useState(null);

useEffect(() => {
  fetchLanguageTheory();
}, []);

const fetchLanguageTheory = async () => {
  try {
    const response = await fetch('/api/language/theory');
    const data = await response.json();
    setLanguageTheory(data);
  } catch (error) {
    console.error('Error fetching language theory:', error);
  }
};

const handleCodeChange = (value) => {
  setCode(value);
};

const analyzeLexer = async () => {
  try {
    const response = await fetch('/api/analyze/lexer', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ code }),
    });
    const data = await response.json();
    setOutput(JSON.stringify(data, null, 2));
    setLastRunTab('lexer');
  } catch (error) {
    setOutput('Error en el análisis léxico: ' + error.message);
  }
};

const analyzeParser = async () => {
  try {
    const response = await fetch('/api/analyze/parser', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ code }),
    });
    const data = await response.json();
    setOutput(JSON.stringify(data, null, 2));
    setLastRunTab('parser');
  } catch (error) {
    setOutput('Error en el análisis sintáctico: ' + error.message);
  }
};

const analyzeSemantic = async () => {
  try {
    const response = await fetch('/api/analyze/semantic', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ code }),
    });
    const data = await response.json();
    setOutput(
      `Código Intermedio:\n${JSON.stringify(data.intermediate_code, null, 2)}\n\n` +
      `Código Generado:\n${data.target_code}`
    );
    setLastRunTab('semantic');
  } catch (error) {
    setOutput('Error en el análisis semántico: ' + error.message);
  }
};

const runProgram = async () => {
  try {
    const response = await fetch('/api/run', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ code }),
    });
    const data = await response.json();
    setOutput(data.output || JSON.stringify(data, null, 2));
    setLastRunTab('run');
  } catch (error) {
    setOutput('Error al ejecutar el programa: ' + error.message);
  }
};

const handleTabClick = (tab) => {
  setActiveTab(tab);
  if (tab === lastRunTab) {
    return;
  }
  if (tab === 'theory') {
    setOutput('');
  }
};

const renderTheory = () => {
  if (!languageTheory) return 'Cargando teoría del lenguaje...';

  return (
    <div className="space-y-8 p-4">
      <div className="bg-gray-800 rounded-lg p-6">
        <h3 className="text-xl font-bold mb-4 text-blue-400">Autómata Finito Determinista (AFD)</h3>
        <div className="bg-gray-900 p-4 rounded overflow-auto h-96">
          <AutomataVisualizer dot={languageTheory.automaton} />
        </div>
      </div>
      
      <div className="bg-gray-800 rounded-lg p-6">
        <h3 className="text-xl font-bold mb-4 text-blue-400">Gramática del Lenguaje</h3>
        <div className="bg-gray-900 p-4 rounded overflow-auto">
          <pre className="whitespace-pre-wrap text-green-300 font-mono text-sm">
            {languageTheory.grammar}
          </pre>
        </div>
      </div>

      <div className="bg-gray-800 rounded-lg p-6">
        <h3 className="text-xl font-bold mb-4 text-blue-400">Traducción Semántica</h3>
        <div className="bg-gray-900 p-4 rounded overflow-auto">
          <pre className="whitespace-pre-wrap text-green-300 font-mono text-sm">
            {`Acciones Semánticas:

1. Declaraciones:
 DECLARE tipo valor variable
 Ejemplo: DECLARE INT 0 x

2. Asignaciones:
 ASSIGN valor_temp None variable
 Ejemplo: ASSIGN t1 None x

3. Operaciones:
 op arg1 arg2 resultado
 Ejemplo: PLUS t1 t2 t3

4. Control de Flujo:
 IF_FALSE condición None etiqueta
 GOTO None None etiqueta
 LABEL None None etiqueta

5. Entrada/Salida:
 PRINT valor_temp
 READ variable`}
          </pre>
        </div>
      </div>
      
      <div className="bg-gray-800 rounded-lg p-6">
        <h3 className="text-xl font-bold mb-4 text-blue-400">Tipos de Tokens</h3>
        <div className="space-y-4">
          {Object.entries(languageTheory.token_types).map(([category, tokens]) => (
            <div key={category} className="bg-gray-900 p-4 rounded">
              <h4 className="font-bold text-purple-400 mb-2">{category}:</h4>
              <div className="ml-4 text-green-300">
                {Array.isArray(tokens) ? (
                  <ul className="list-disc list-inside">
                    {tokens.map((token, index) => (
                      <li key={index}>{token}</li>
                    ))}
                  </ul>
                ) : (
                  <p>{tokens}</p>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

return (
  <div className="h-screen bg-gray-900 text-white">
    <nav className="bg-gray-800 p-4">
      <h1 className="text-2xl font-bold">Editor Lenguaje Francés</h1>
    </nav>
    
    <PanelGroup direction="horizontal" className="h-[calc(100vh-64px)]">
      <Panel defaultSize={50} minSize={30}>
        <div className="h-full p-4">
          <CodeMirror
            value={code}
            height="100%"
            theme={oneDark}
            extensions={[python()]}
            onChange={handleCodeChange}
          />
        </div>
      </Panel>
      
      <PanelResizeHandle className="w-2 bg-gray-700 hover:bg-blue-600 transition-colors" />
      
      <Panel minSize={30}>
        <div className="h-full flex flex-col">
          <div className="bg-gray-800 p-4 flex space-x-4">
            <button
              onClick={() => {
                handleTabClick('lexer');
                analyzeLexer();
              }}
              className={`flex items-center px-4 py-2 rounded transition-colors ${
                activeTab === 'lexer' ? 'bg-blue-600' : 'bg-gray-700 hover:bg-gray-600'
              }`}
            >
              <FaCode className="mr-2" /> Análisis Léxico
            </button>
            <button
              onClick={() => {
                handleTabClick('parser');
                analyzeParser();
              }}
              className={`flex items-center px-4 py-2 rounded transition-colors ${
                activeTab === 'parser' ? 'bg-blue-600' : 'bg-gray-700 hover:bg-gray-600'
              }`}
            >
              <FaTree className="mr-2" /> Análisis Sintáctico
            </button>
            <button
              onClick={() => {
                handleTabClick('semantic');
                analyzeSemantic();
              }}
              className={`flex items-center px-4 py-2 rounded transition-colors ${
                activeTab === 'semantic' ? 'bg-blue-600' : 'bg-gray-700 hover:bg-gray-600'
              }`}
            >
              <FaCogs className="mr-2" /> Análisis Semántico
            </button>
            <button
              onClick={() => handleTabClick('theory')}
              className={`flex items-center px-4 py-2 rounded transition-colors ${
                activeTab === 'theory' ? 'bg-blue-600' : 'bg-gray-700 hover:bg-gray-600'
              }`}
            >
              <FaBook className="mr-2" /> Teoría
            </button>
            <button
              onClick={() => {
                runProgram();
                setLastRunTab('run');
              }}
              className="flex items-center px-4 py-2 rounded bg-green-600 hover:bg-green-700 transition-colors"
            >
              <FaPlay className="mr-2" /> Ejecutar
            </button>
          </div>
          
          <div className="flex-1 p-4 bg-gray-800 overflow-auto">
            {activeTab === 'theory' ? (
              renderTheory()
            ) : (
              <pre className="font-mono text-sm bg-gray-900 p-4 rounded">
                {output || 'El resultado del análisis aparecerá aquí...'}
              </pre>
            )}
          </div>
        </div>
      </Panel>
    </PanelGroup>
  </div>
);
}

export default App;