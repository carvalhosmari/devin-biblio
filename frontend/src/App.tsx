/**
 * App principal do Bibliomania.
 * Template raiz do padrao MVT (camada de apresentacao).
 */

import LeitorPage from "./components/Leitor";
import LivroPage from "./components/Livro";
import EmprestimoPage from "./components/Emprestimo";

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-indigo-700 text-white p-4 shadow-md">
        <h1 className="text-3xl font-bold text-center">Bibliomania</h1>
        <p className="text-center text-indigo-200 text-sm">
          Sistema de Gestao de Biblioteca
        </p>
      </header>

      <main className="max-w-7xl mx-auto p-6 space-y-8">
        <section>
          <LeitorPage />
        </section>
        <section>
          <EmprestimoPage />
        </section>
        <section>
          <LivroPage />
        </section>
      </main>
    </div>
  );
}

export default App;
