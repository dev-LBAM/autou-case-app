import { useState, useRef, useEffect } from "react";
import type { ChangeEvent, FormEvent } from "react";

interface ResponseData {
  category: string;
  suggested_response: string;
  timestamp: string;
}

type Mode = "text" | "file" | null;

const LOCAL_STORAGE_KEY = "email_responses";

const EmailProcessor: React.FC = () => {
  const [mode, setMode] = useState<Mode>(null);
  const [content, setContent] = useState<string>("");
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [progress, setProgress] = useState<number>(15);
  const [abortController, setAbortController] = useState<AbortController | null>(null);

  const [responses, setResponses] = useState<ResponseData[]>(() => {
    try {
      const saved = localStorage.getItem(LOCAL_STORAGE_KEY);
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });

  const [error, setError] = useState<string>("");
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);
  const [visibleCount, setVisibleCount] = useState(5);

  const fileInputRef = useRef<HTMLInputElement>(null);
  const historyRef = useRef<HTMLDivElement>(null);
  const cardRefs = useRef<(HTMLDivElement | null)[]>([]);
  const prevLength = useRef<number>(responses.length);

  useEffect(() => {
    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(responses));
  }, [responses]);

  const handleModeChange = (newMode: Mode) => {
    setMode(newMode);
    setError("");
    if (newMode === "text") {
      setFile(null);
      if (fileInputRef.current) fileInputRef.current.value = "";
    } else if (newMode === "file") {
      setContent("");
    }
  };

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.[0]) setFile(e.target.files[0]);
  };

  const handleContentChange = (e: ChangeEvent<HTMLTextAreaElement>) => {
    setContent(e.target.value);
  };

  const handleCopy = (text: string, index: number) => {
    navigator.clipboard.writeText(text);
    setCopiedIndex(index);
    setTimeout(() => setCopiedIndex(null), 1500);
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    setContent("");
    setFile(null);

    const controller = new AbortController();
    setAbortController(controller);

    setProgress(0); // zera a barra
  const progressInterval = setInterval(() => {
    setProgress((prev) => (prev < 95 ? prev + 1 : prev)); // vai até 95% enquanto espera
  }, 50);


    try {
      let res: Response;
      if (mode === "file" && file) {
        const formData = new FormData();
        formData.append("file", file);
        res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/process_email/file`, {
          method: "POST",
          body: formData,
          signal: controller.signal,
        });
      } else if (mode === "text" && content.trim()) {
        res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/process_email`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ content }),
          signal: controller.signal,
        });
      } else {
        setError("Por favor, escolha uma opção e forneça os dados.");
        setLoading(false);
        return;
      }

      clearInterval(progressInterval);
      setProgress(100); 

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Erro desconhecido");
      }

      const data: ResponseData = await res.json();
      const formatted: ResponseData = {
        ...data,
        timestamp: new Date().toLocaleString("pt-BR", {
          day: "2-digit",
          month: "2-digit",
          year: "numeric",
          hour: "2-digit",
          minute: "2-digit",
        }),
      };
      setTimeout(() => setResponses((prev) => [formatted, ...prev]), 700);
    } catch (err: any) {
      if (err.name === "AbortError") {
        setError("Processamento cancelado.");
      } else {
        setError(err.message);
      }
    } finally {
      setTimeout(() => setLoading(false), 500);
      setTimeout(() => setProgress(0), 600);
      setAbortController(null);
    }
  };

  const handleCancel = () => {
    abortController?.abort();
  };

  const showMore = () => setVisibleCount((prev) => prev + 5);

  useEffect(() => {
    if (responses.length > prevLength.current && cardRefs.current[0]) {
      cardRefs.current[0].scrollIntoView({ behavior: "smooth" });
    }
    prevLength.current = responses.length;
  }, [responses]);

  return (
    <div className="min-h-screen flex items-start justify-center bg-gray-900 p-6">
      <div className="w-full max-w-4xl bg-gray-800 text-gray-100 rounded-2xl p-10 shadow-2xl">
        <h1 className="text-4xl font-extrabold text-center text-indigo-400 mb-3">
          Processador de Emails
        </h1>
        <p className="text-center text-gray-300 mb-8">
          Classifique emails em{" "}
          <span className="font-semibold text-indigo-300">Produtivo</span> ou{" "}
          <span className="font-semibold text-pink-400">Improdutivo</span> e receba respostas automáticas.
        </p>

        <div className="grid grid-cols-2 gap-6 mb-8">
          <button
            type="button"
            onClick={() => handleModeChange("text")}
            className={`p-6 rounded-xl border-2 transition-all duration-300 transform ${
              mode === "text"
                ? "border-indigo-400 bg-gray-700 scale-105 shadow-md"
                : "border-gray-600 hover:border-indigo-500 hover:scale-105"
            }`}
          >
            <span className="block text-xl font-semibold">✍️ Digitar Texto</span>
            <span className="text-sm text-gray-400">Escreva manualmente o conteúdo do email</span>
          </button>

          <button
            type="button"
            onClick={() => handleModeChange("file")}
            className={`p-6 rounded-xl border-2 transition-all duration-300 transform ${
              mode === "file"
                ? "border-indigo-400 bg-gray-700 scale-105 shadow-md"
                : "border-gray-600 hover:border-indigo-500 hover:scale-105"
            }`}
          >
            <span className="block text-xl font-semibold">📂 Enviar Arquivo</span>
            <span className="text-sm text-gray-400">Suporta arquivos .txt e .pdf</span>
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {mode === "text" && (
            <div>
              <label className="block text-gray-300 font-semibold mb-2">Digite o conteúdo do email:</label>
              <textarea
                className="w-full p-4 border border-gray-600 rounded-xl bg-gray-700 text-gray-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="Escreva seu email aqui..."
                value={content}
                onChange={handleContentChange}
                rows={6}
              />
            </div>
          )}

          {mode === "file" && (
            <div>
              <label className="block text-gray-300 font-semibold mb-2">Selecione o arquivo:</label>
              <input
                ref={fileInputRef}
                type="file"
                accept=".txt,.pdf"
                onChange={handleFileChange}
                className="block w-full text-sm text-gray-100 border border-gray-600 rounded-xl cursor-pointer file:mr-4 file:py-2 file:px-4 file:border-0 file:rounded-md file:bg-indigo-600 file:text-white hover:file:bg-indigo-700"
              />
              {file && <p className="mt-2 text-sm text-gray-400">📄 {file.name}</p>}
            </div>
          )}

          <div className="flex gap-4">
            <button
              type="submit"
              className={`flex-1 py-3 px-4 bg-indigo-600 text-white font-bold rounded-xl shadow transition-all ${
                loading ? "cursor-wait opacity-50" : ""
              }`}
              disabled={loading}
            >
              {loading ? "Processando..." : "Enviar"}
            </button>

            {loading && (
              <button
                type="button"
                onClick={handleCancel}
                className="py-3 px-4 bg-red-600 text-white font-bold rounded-xl shadow hover:bg-red-700 transition-all"
              >
                Cancelar
              </button>
            )}
          </div>
        </form>

        {loading && (
          <div className="mt-6">
            <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
              <div
                className="bg-indigo-600 h-2 rounded-full transition-all duration-500 progress-striped"
                style={{ width: `${progress}%` }}
              ></div>
            </div>
          </div>
        )}

        {error && <p className="text-red-500 mt-6 text-center">{error}</p>}

        <div className="mt-8">
          <h2 className="text-2xl font-bold text-indigo-400 mb-4">📜 Histórico</h2>

          <div
            ref={historyRef}
            className="h-[400px] overflow-y-auto p-4 bg-gray-900 border border-gray-700 rounded-xl shadow-inner space-y-4"
          >
            {responses.length === 0 && (
              <p className="text-gray-500 text-center">Nenhuma resposta processada ainda.</p>
            )}
{responses.slice(0, visibleCount).map((resp, index) => (
  <div
    key={index}
    ref={(el: HTMLDivElement | null) => {
      cardRefs.current[index] = el;
    }}
    className="p-4 bg-gray-800 rounded-xl shadow border border-gray-700"
    style={{ scrollMarginTop: "20px" }} // <- distância do topo ao rolar
  >
    <p className="text-sm text-gray-400 mb-2">{resp.timestamp}</p>

    <p className="text-lg">
      <span className="font-semibold text-yellow-200">Categoria:</span>{" "}
      <span
        className={`font-bold ${
          resp.category === "Produtivo" ? "text-indigo-300" : "text-pink-400"
        }`}
      >
        {resp.category}
      </span>
    </p>
    <p className="mt-2 text-lg">
      <span className="font-semibold text-yellow-200">Resposta Sugerida:</span>{" "}
      <span className="text-gray-200">{resp.suggested_response}</span>
    </p>
    <button
      onClick={() => handleCopy(resp.suggested_response, index)}
      className="mt-3 px-3 py-1 text-sm bg-indigo-600 text-white rounded-md shadow hover:bg-indigo-700 relative"
    >
      {copiedIndex === index ? "✔ Copiado" : "Copiar Resposta"}
    </button>
  </div>
))}


            {visibleCount < responses.length && (
              <button
                onClick={showMore}
                className="mt-2 w-full py-2 text-sm text-indigo-400 hover:underline bg-gray-800 rounded-md"
              >
                Mostrar mais
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default EmailProcessor;
