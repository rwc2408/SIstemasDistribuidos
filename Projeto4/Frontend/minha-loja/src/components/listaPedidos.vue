<template>
  <div>
    <h2>Lista de Pedidos</h2>
    <ul>
      <li v-for="order in orders" :key="order.pedido_id" class="order-item">
        <h3>Pedido {{ order.pedido_id }} - Status: {{ order.status }}</h3>

        <button @click="order.mostrarDetalhes = !order.mostrarDetalhes">
          {{ order.mostrarDetalhes ? 'Ocultar Detalhes' : 'Ver Detalhes' }}
        </button>

        <div v-if="order.mostrarDetalhes" class="order-details">
          <ul>
            <li v-for="item in order.produtos" :key="item.produto_id">
              <p>
                <strong>{{ item.nome }}</strong> — {{ item.quantidade }} x R$ {{ item.preco.toFixed(2) }}
              </p>
            </li>
          </ul>
          <p class="order-total">Total: R$ {{ calcularTotal(order.produtos) }}</p>
        </div>

        <div class="order-actions">
          <button v-if="order.status === 'Criado'" @click="iniciarPagamento(order)">
            Efetuar Pagamento
          </button>
          <button @click="excluirPedido(order.pedido_id)" class="delete-button">
            Excluir Pedido
          </button>
        </div>
      </li>
    </ul>

    <div v-if="notification" class="notification">
      <p>Notificação: {{ notification }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

let sseClient;

export default {
  data() {
    return {
      orders: [],
      notification: null,
    };
  },

  async created() {
    await this.carregarPedidos();
    this.conectarNotificacoes();
  },

  methods: {
    calcularTotal(produtos) {
      return produtos.reduce(
        (total, item) => total + item.quantidade * item.preco,
        0
      ).toFixed(2);
    },

    async carregarPedidos() {
      try {
        const response = await axios.get("http://localhost:5000/pedidos");
        this.orders = response.data.map((order) => ({
          ...order,
          mostrarDetalhes: false,
        }));
      } catch (error) {
        console.error("Erro ao carregar pedidos:", error);
      }
    },

    conectarNotificacoes() {
      if (!this.$sse) {
        console.error("Erro: Plugin VueSSE não está configurado.");
        return;
      }

      sseClient = this.$sse.create({
        url: "http://localhost:5005/notificacoes",
        format: "json",
      });

      sseClient.on("message", (data) => {
        this.notification = `Pedido ${data.pedido_id} atualizado para ${data.status}`;
        const pedido = this.orders.find((order) => order.pedido_id === data.pedido_id);
        if (pedido) {
          pedido.status = data.status;
        }
      });

      sseClient.on("error", (err) => {
        console.error("Erro no SSE:", err);
      });

      sseClient.connect().then(() => {
        console.log("Conexão SSE estabelecida.");
      });
    },

    async iniciarPagamento(pedido) {
      try {
        const payload = pedido;
        const response = await axios.post(
          `http://localhost:5002/pagamento/${pedido.pedido_id}`,
          payload
        );
        if (response.status === 200) {
          alert(`Pagamento iniciado para o pedido ${pedido.pedido_id}!`);
        }
      } catch (error) {
        alert("Erro ao iniciar pagamento.");
      }
    },

    async excluirPedido(pedidoId) {
      try {
        if (confirm(`Deseja realmente excluir o pedido ${pedidoId}?`)) {
          await axios.delete(`http://localhost:5000/pedidos/${pedidoId}`);
          this.orders = this.orders.filter((order) => order.pedido_id !== pedidoId);
          alert(`Pedido ${pedidoId} excluído com sucesso!`);
        }
      } catch {
        alert("Erro ao excluir pedido.");
      }
    },
  },

  beforeUnmount() {
    if (sseClient) {
      sseClient.disconnect();
      console.log("Conexão SSE encerrada.");
    }
  },
};
</script>

<style>
.order-item {
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 15px;
  margin-bottom: 20px;
  background-color: #ffffff;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

h3 {
  color: #333;
}

.order-details ul {
  padding-left: 0;
}

.order-details li {
  color: #444;
  font-size: 0.95em;
}

.order-total {
  font-weight: bold;
  color: #000;
}

button {
  background-color: #007bff;
  padding: 8px 12px;
  border: none;
  color: white;
  cursor: pointer;
  border-radius: 5px;
  margin-right: 5px;
}

button:hover {
  background-color: #0056b3;
}

.delete-button {
  background-color: #dc3545;
}

.delete-button:hover {
  background-color: #c82333;
}
</style>
