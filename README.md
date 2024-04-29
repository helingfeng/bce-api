给RAG社区一个可以直接拿来用，尽可能不需要用户finetune的中英双语和跨语种二阶段检索模型库，包含`EmbeddingModel`和`RerankerModel`。

- 只需一个模型：`EmbeddingModel`覆盖 **中英双语和中英跨语种** 检索任务，尤其是其跨语种能力。`RerankerModel`支持 **中英日韩** 四个语种及其跨语种。
- 只需一个模型： **覆盖常见业务落地领域**（针对众多常见rag场景已做优化），比如：教育、医疗、法律、金融、科研论文、客服(FAQ)、书籍、百科、通用QA等场景。用户不需要在上述特定领域finetune，直接可以用。
- 方便集成：`EmbeddingModel`和`RerankerModel`提供了LlamaIndex和LangChain **集成接口** ，用户可非常方便集成进现有产品中。
- 其他特性：
  - `RerankerModel`支持 **长passage（超过512 tokens，不超过32k tokens）rerank**；
  - `RerankerModel`可以给出有意义 **相关性分数** ，帮助 **过滤低质量召回**；
  - `EmbeddingModel` **不需要“精心设计”instruction** ，尽可能召回有用片段。