/**
 * Tipos do sistema Bibliomania.
 * Sera implementado nos proximos PRs.
 */

/** Leitor (Reader) */
export interface Leitor {
  id: number;
  nome: string;
  email: string;
  telefone?: string;
  endereco?: string;
  data_cadastro: string;
  ativo: boolean;
}

/** Livro (Book) */
export interface Livro {
  id: number;
  isbn: string;
  titulo: string;
  autores: string;
  pais?: string;
  editora?: string;
  edicao?: string;
  status: string;
}

/** Emprestimo (Loan) */
export interface Emprestimo {
  id: number;
  id_leitor: number;
  id_livro: number;
  data_emprestimo: string;
  data_devolucao?: string;
  data_limite: string;
  status: string;
}
