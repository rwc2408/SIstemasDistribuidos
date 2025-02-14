<template>
  <div>
    <h1>Bem vindo à Loja</h1>
    <button @click="navigateTo('listaProdutos')">Lista de Produtos</button>
    <button @click="navigateTo('listaPedidos')">Lista de Pedidos</button>
    <button @click="navigateTo('carrinho')">Ir para o Carrinho ({{ cartItemCount }} itens)</button>
    <component :is="currentComponent" />
  </div>
</template>

<script>
import listaProdutos from './listaProdutos.vue';
import carrinho from './carrinho.vue';
import listaPedidos from './listaPedidos.vue';
import axios from 'axios';

export default {
  data() {
    return {
      currentComponent: null,
      cartItemCount: 0,
    };
  },
  methods: {
    async navigateTo(component) {
      this.currentComponent = component;
      if (component === 'carrinho') {
        await this.atualizarCarrinho();
      }
    },
    async atualizarCarrinho() {
      try {
        const response = await axios.get('http://localhost:5000/carrinho');
        this.cartItemCount = response.data.length;
      } catch (error) {
        console.error('Erro ao carregar carrinho:', error);
      }
    },
  },
  components: {
    listaProdutos,
    carrinho,
    listaPedidos,
  },
  created() {
    this.atualizarCarrinho();
  },
};
</script>
