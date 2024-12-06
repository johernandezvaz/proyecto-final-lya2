import PropTypes from 'prop-types';
import { Graphviz } from 'graphviz-react';

function AutomataVisualizer({ dot }) {
  if (!dot) {
    return (
      <div className="w-full h-full flex items-center justify-center bg-gray-100 rounded-lg">
        <p className="text-gray-500">No hay datos del autómata disponibles</p>
      </div>
    );
  }

  return (
    <div className="w-full h-full overflow-auto bg-white rounded-lg p-4">
      <Graphviz
        dot={dot}
        options={{
          zoom: true,
          width: "100%",
          height: "100%",
          fit: true,
          engine: "dot",
          useWorker: false
        }}
      />
    </div>
  );
}

AutomataVisualizer.propTypes = {
  dot: PropTypes.string
};

AutomataVisualizer.defaultProps = {
  dot: ''
};

export default AutomataVisualizer;