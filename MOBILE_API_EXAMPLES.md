# Exemplos de Uso da API - App Mobile

## **📱 Flutter/Dart**

### **Configuração Inicial:**
```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class HelpOPApi {
  static const String baseUrl = 'http://localhost:8000/api';
  static String? sessionId;
  
  static Map<String, String> get headers => {
    'Content-Type': 'application/json',
    if (sessionId != null) 'Cookie': 'sessionid=$sessionId',
  };
  
  static void setSessionId(String id) {
    sessionId = id;
  }
}
```

### **Login e Autenticação:**
```dart
class AuthService {
  static Future<bool> login(String username, String password) async {
    try {
      final response = await http.post(
        Uri.parse('http://localhost:8000/login/'),
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: {
          'username': username,
          'password': password,
        },
      );
      
      if (response.statusCode == 302) {
        // Extrair sessionid do cookie
        final cookies = response.headers['set-cookie'];
        if (cookies != null) {
          final sessionMatch = RegExp(r'sessionid=([^;]+)').firstMatch(cookies);
          if (sessionMatch != null) {
            HelpOPApi.setSessionId(sessionMatch.group(1)!);
            return true;
          }
        }
      }
      return false;
    } catch (e) {
      print('Erro no login: $e');
      return false;
    }
  }
}
```

### **Gerenciar Veículos:**
```dart
class VeiculoService {
  static Future<List<Veiculo>> getVeiculos() async {
    try {
      final response = await http.get(
        Uri.parse('${HelpOPApi.baseUrl}/veiculos/'),
        headers: HelpOPApi.headers,
      );
      
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return (data['results'] as List)
            .map((json) => Veiculo.fromJson(json))
            .toList();
      }
      throw Exception('Falha ao carregar veículos');
    } catch (e) {
      print('Erro: $e');
      return [];
    }
  }
  
  static Future<Veiculo?> createVeiculo(Map<String, dynamic> veiculoData) async {
    try {
      final response = await http.post(
        Uri.parse('${HelpOPApi.baseUrl}/veiculos/'),
        headers: HelpOPApi.headers,
        body: json.encode(veiculoData),
      );
      
      if (response.statusCode == 201) {
        return Veiculo.fromJson(json.decode(response.body));
      }
      return null;
    } catch (e) {
      print('Erro ao criar veículo: $e');
      return null;
    }
  }
}

class Veiculo {
  final int id;
  final String marca;
  final String modelo;
  final int ano;
  final String placa;
  final int kmAtual;
  
  Veiculo({
    required this.id,
    required this.marca,
    required this.modelo,
    required this.ano,
    required this.placa,
    required this.kmAtual,
  });
  
  factory Veiculo.fromJson(Map<String, dynamic> json) {
    return Veiculo(
      id: json['id'],
      marca: json['marca'],
      modelo: json['modelo'],
      ano: json['ano'],
      placa: json['placa'],
      kmAtual: json['km_atual'],
    );
  }
}
```

### **Gerenciar Checklists:**
```dart
class ChecklistService {
  static Future<List<Checklist>> getChecklists() async {
    try {
      final response = await http.get(
        Uri.parse('${HelpOPApi.baseUrl}/checklists/'),
        headers: HelpOPApi.headers,
      );
      
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return (data['results'] as List)
            .map((json) => Checklist.fromJson(json))
            .toList();
      }
      throw Exception('Falha ao carregar checklists');
    } catch (e) {
      print('Erro: $e');
      return [];
    }
  }
  
  static Future<Checklist?> getChecklistDetalhado(int id) async {
    try {
      final response = await http.get(
        Uri.parse('${HelpOPApi.baseUrl}/checklists/$id/detalhado/'),
        headers: HelpOPApi.headers,
      );
      
      if (response.statusCode == 200) {
        return Checklist.fromJson(json.decode(response.body));
      }
      return null;
    } catch (e) {
      print('Erro ao carregar checklist: $e');
      return null;
    }
  }
  
  static Future<ChecklistExecutado?> executarChecklist(Map<String, dynamic> data) async {
    try {
      final response = await http.post(
        Uri.parse('${HelpOPApi.baseUrl}/checklists-executados/'),
        headers: HelpOPApi.headers,
        body: json.encode(data),
      );
      
      if (response.statusCode == 201) {
        return ChecklistExecutado.fromJson(json.decode(response.body));
      }
      return null;
    } catch (e) {
      print('Erro ao executar checklist: $e');
      return null;
    }
  }
}

class Checklist {
  final int id;
  final String nome;
  final String descricao;
  final bool ativo;
  final String oficinaNome;
  final String tipoVeiculoNome;
  final List<ItemChecklistPersonalizado> itens;
  
  Checklist({
    required this.id,
    required this.nome,
    required this.descricao,
    required this.ativo,
    required this.oficinaNome,
    required this.tipoVeiculoNome,
    required this.itens,
  });
  
  factory Checklist.fromJson(Map<String, dynamic> json) {
    return Checklist(
      id: json['id'],
      nome: json['nome'],
      descricao: json['descricao'] ?? '',
      ativo: json['ativo'],
      oficinaNome: json['oficina_nome'],
      tipoVeiculoNome: json['tipo_veiculo_nome'],
      itens: (json['itens_personalizados'] as List?)
          ?.map((item) => ItemChecklistPersonalizado.fromJson(item))
          .toList() ?? [],
    );
  }
}

class ItemChecklistPersonalizado {
  final int id;
  final String nome;
  final String descricao;
  final String categoriaNome;
  final String tipoVerificacao;
  final bool critico;
  final bool obrigatorio;
  
  ItemChecklistPersonalizado({
    required this.id,
    required this.nome,
    required this.descricao,
    required this.categoriaNome,
    required this.tipoVerificacao,
    required this.critico,
    required this.obrigatorio,
  });
  
  factory ItemChecklistPersonalizado.fromJson(Map<String, dynamic> json) {
    return ItemChecklistPersonalizado(
      id: json['id'],
      nome: json['nome'],
      descricao: json['descricao'] ?? '',
      categoriaNome: json['categoria_nome'],
      tipoVerificacao: json['tipo_verificacao'],
      critico: json['critico'],
      obrigatorio: json['obrigatorio'],
    );
  }
}
```

## **📱 React Native**

### **Configuração Inicial:**
```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para adicionar cookies de sessão
api.interceptors.request.use((config) => {
  const sessionId = AsyncStorage.getItem('sessionId');
  if (sessionId) {
    config.headers.Cookie = `sessionid=${sessionId}`;
  }
  return config;
});

export default api;
```

### **Serviços de Autenticação:**
```javascript
import AsyncStorage from '@react-native-async-storage/async-storage';

export const AuthService = {
  async login(username, password) {
    try {
      const response = await axios.post('http://localhost:8000/login/', {
        username,
        password,
      }, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });
      
      if (response.status === 302) {
        const cookies = response.headers['set-cookie'];
        if (cookies) {
          const sessionMatch = cookies.match(/sessionid=([^;]+)/);
          if (sessionMatch) {
            await AsyncStorage.setItem('sessionId', sessionMatch[1]);
            return true;
          }
        }
      }
      return false;
    } catch (error) {
      console.error('Erro no login:', error);
      return false;
    }
  },
  
  async logout() {
    await AsyncStorage.removeItem('sessionId');
  },
};
```

### **Serviços de Checklist:**
```javascript
export const ChecklistService = {
  async getChecklists() {
    try {
      const response = await api.get('/checklists/');
      return response.data.results;
    } catch (error) {
      console.error('Erro ao carregar checklists:', error);
      return [];
    }
  },
  
  async getChecklistDetalhado(id) {
    try {
      const response = await api.get(`/checklists/${id}/detalhado/`);
      return response.data;
    } catch (error) {
      console.error('Erro ao carregar checklist:', error);
      return null;
    }
  },
  
  async executarChecklist(data) {
    try {
      const response = await api.post('/checklists-executados/', data);
      return response.data;
    } catch (error) {
      console.error('Erro ao executar checklist:', error);
      return null;
    }
  },
  
  async atualizarItemExecutado(id, data) {
    try {
      const response = await api.put(`/itens-checklist-executados/${id}/`, data);
      return response.data;
    } catch (error) {
      console.error('Erro ao atualizar item:', error);
      return null;
    }
  },
};
```

### **Componente de Checklist:**
```javascript
import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, TouchableOpacity, Alert } from 'react-native';
import { ChecklistService } from '../services/ChecklistService';

const ChecklistScreen = () => {
  const [checklists, setChecklists] = useState([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    loadChecklists();
  }, []);
  
  const loadChecklists = async () => {
    try {
      setLoading(true);
      const data = await ChecklistService.getChecklists();
      setChecklists(data);
    } catch (error) {
      Alert.alert('Erro', 'Falha ao carregar checklists');
    } finally {
      setLoading(false);
    }
  };
  
  const executarChecklist = async (checklistId, veiculoId) => {
    try {
      const data = {
        checklist: checklistId,
        veiculo: veiculoId,
        observacoes: 'Executado via app mobile',
      };
      
      const resultado = await ChecklistService.executarChecklist(data);
      if (resultado) {
        Alert.alert('Sucesso', 'Checklist iniciado com sucesso!');
        // Navegar para tela de execução
      }
    } catch (error) {
      Alert.alert('Erro', 'Falha ao executar checklist');
    }
  };
  
  const renderChecklist = ({ item }) => (
    <TouchableOpacity
      style={styles.checklistItem}
      onPress={() => executarChecklist(item.id, 1)} // veiculoId = 1
    >
      <Text style={styles.checklistNome}>{item.nome}</Text>
      <Text style={styles.checklistOficina}>{item.oficina_nome}</Text>
      <Text style={styles.checklistTipo}>{item.tipo_veiculo_nome}</Text>
    </TouchableOpacity>
  );
  
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Checklists Disponíveis</Text>
      <FlatList
        data={checklists}
        renderItem={renderChecklist}
        keyExtractor={(item) => item.id.toString()}
        refreshing={loading}
        onRefresh={loadChecklists}
      />
    </View>
  );
};

const styles = {
  container: {
    flex: 1,
    padding: 16,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 16,
  },
  checklistItem: {
    padding: 16,
    backgroundColor: '#f0f0f0',
    marginBottom: 8,
    borderRadius: 8,
  },
  checklistNome: {
    fontSize: 18,
    fontWeight: 'bold',
  },
  checklistOficina: {
    fontSize: 14,
    color: '#666',
  },
  checklistTipo: {
    fontSize: 12,
    color: '#999',
  },
};

export default ChecklistScreen;
```

## **🎯 Próximos Passos para o Mobile**

1. **Implementar autenticação por token** para maior segurança
2. **Adicionar cache offline** para funcionar sem internet
3. **Implementar push notifications** para notificações
4. **Adicionar upload de fotos** para itens de checklist
5. **Criar sincronização offline** para dados não enviados
6. **Implementar geolocalização** para oficinas próximas

## **🚀 API Pronta para Mobile!**

A API está **100% funcional** e pronta para integração com aplicativos mobile! ✨📱 