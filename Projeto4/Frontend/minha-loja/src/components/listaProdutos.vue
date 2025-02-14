<template>
  <div class="products-list">
    <h1>Lista de Produtos</h1>
    <ul>
      <li v-for="produto in produtos" :key="produto.id" class="product-item">
        {{ produto.nome }} - R$ {{ produto.preco.toFixed(2) }}
        <div class="quantity-control">
          <button @click="decrementarQuantidade(produto)">-</button>
          <span>{{ produto.quantidadeSelecionada }}</span>
          <button @click="incrementarQuantidade(produto)">+</button>
        </div>
      </li>
    </ul>
    <button 
      class="adicionar-carrinho-btn" 
      @click="confirmarAdicao" 
      :disabled="!temProdutosSelecionados"
    >
      Adicionar ao Carrinho
    </button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      produtos: [],
    };
  },
  computed: {
    temProdutosSelecionados() {
      // Verifica se há pelo menos um produto com quantidade maior que zero
      return this.produtos.some(produto => produto.quantidadeSelecionada > 0);
    },
  },
  methods: {
    async listarProdutos() {
      try {
        const response = await axios.get('http://localhost:5000/produtos');
        this.produtos = response.data.map(produto => ({
          ...produto,
          quantidadeSelecionada: 0
        }));
      } catch (error) {
        console.error('Erro ao listar produtos:', error);
      }
    },
    incrementarQuantidade(produto) {
      produto.quantidadeSelecionada++;
    },
    decrementarQuantidade(produto) {
      if (produto.quantidadeSelecionada > 0) {
        produto.quantidadeSelecionada--;
      }
    },
    async confirmarAdicao() {
      const produtosSelecionados = this.produtos.filter(produto => produto.quantidadeSelecionada > 0);

      for (const produto of produtosSelecionados) {
        const item = {
          produto_id: produto.id,
          nome: produto.nome,
          preco: produto.preco,
          quantidade: produto.quantidadeSelecionada,
        };
        
        try {
          const response = await axios.post('http://localhost:5000/carrinho', item);
          if (response.status === 201) {
            alert(`Adicionado ${produto.quantidadeSelecionada} unidade(s) de "${produto.nome}" ao carrinho!`);
          }
        } catch (error) {
          console.error('Erro ao adicionar ao carrinho:', error);
        }

        // Reset da quantidade após adicionar ao carrinho
        produto.quantidadeSelecionada = 0;
      }
    },
  },
  created() {
    this.listarProdutos();
  },
};
</script>

<style>
.products-list {
  padding: 20px;
}
.product-item {
  margin: 10px 0;
}
.quantity-control {
  display: flex;
  align-items: center;
  margin: 5px 0;
}
.quantity-control button {
  width: 30px;
  height: 30px;
  margin: 0 5px;
}
.adicionar-carrinho-btn {
  margin-top: 20px;
  padding: 10px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
}
.adicionar-carrinho-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>
