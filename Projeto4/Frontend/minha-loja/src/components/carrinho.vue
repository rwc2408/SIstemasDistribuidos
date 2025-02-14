<template>
  <div>
    <h2>Seu Carrinho</h2>
    <ul>
      <li v-for="item in cart" :key="item.produto_id">
        {{ item.nome }} - {{ item.quantidade }} x R$ {{ item.preco }} = R$ {{ (item.quantidade * item.preco).toFixed(2) }}
        <button @click="removerProduto(item)">Remover</button>
      </li>
    </ul>
    <p>Total: R$ {{ total.toFixed(2) }}</p>

    <button @click="finalizarPedido" :disabled="cart.length === 0">
      Criar Pedido
    </button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      cart: [],
    };
  },
  computed: {
    total() {
      return this.cart.reduce((sum, item) => sum + item.quantidade * item.preco, 0);
    },
  },
  methods: {
    async carregarCarrinho() {
      try {
        const response = await axios.get('http://localhost:5000/carrinho');
        this.cart = response.data;
      } catch (error) {
        console.error('Erro ao carregar carrinho:', error);
      }
    },
    async removerProduto(item) {
      try {
        const response = await axios.delete('http://localhost:5000/carrinho', {
          data: { produto_id: item.produto_id },
        });
        if (response.status === 200) {
          this.cart = this.cart.filter(i => i.produto_id !== item.produto_id);
          alert(`Produto "${item.nome}" removido do carrinho.`);
        }
      } catch (error) {
        console.error('Erro ao remover produto do carrinho:', error);
      }
    },
    async finalizarPedido() {
      try {
        const pedido = {
          produtos: this.cart.map(item => ({
            produto_id: item.produto_id,
            nome: item.nome,
            preco: item.preco,
            quantidade: item.quantidade,
          })),
          total: this.total,
        };

        const response = await axios.post('http://localhost:5000/pedidos', pedido);

        if (response.status === 201) {
          alert('Pedido criado com sucesso!');

          // Após criar o pedido, limpa o carrinho no backend
          await axios.delete('http://localhost:5000/esvaziaCarrinho');

          this.cart = []; // Limpa o carrinho após a finalização
        }
      } catch (error) {
        console.error('Erro ao finalizar pedido:', error);
      }
    },
  },
  async created() {
    this.carregarCarrinho();
  },
};
</script>

<style>
ul {
  list-style: none;
  padding: 0;
}
li {
  margin: 10px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
button {
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
  padding: 8px 12px;
  margin-top: 10px;
  border-radius: 5px;
}
button:hover {
  background-color: #0056b3;
}
button[disabled] {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style>
