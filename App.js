import axios from "axios";

const ServerSide = () => {
    const gerarArray = () => {
        axios.post('http://127.0.0.1:5000/create-array')
            .then(response => {
                console.log('Resposta do servidor:', response.data);
            })
            .catch(error => {
                console.error('Erro ao acessar o servidor:', error);
            });
    };

    const ordenarArray = () => {
      axios.get('http://127.0.0.1:5000/ordenar-array')
          .then(response => {
              console.log('Resposta do servidor:', response.data);
          })
          .catch(error => {
              console.error('Erro ao acessar o servidor:', error);
          });
  };

    return (
  <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
      <button onClick={gerarArray}>
          Acessar Servidor - Geração de Array
      </button>
      < br/>
      <button onClick={ordenarArray}>
          Acessar Servidor - Ordenação de Array
      </button>
  </div>
    );
};

export default ServerSide;
