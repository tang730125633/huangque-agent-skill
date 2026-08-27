# Huangque Agent Skill

让 DeepSeek Harness、Codex、OpenClaw 和 Pi Agent 安全调用黄雀 CLI，并通过同一份能力清单提供标准 MCP 工具。

## 仓库边界

- [`huangque-cli`](https://github.com/tang730125633/huangque-cli) 是执行层：鉴权、能力目录、参数校验、报价、确认、任务和结果。
- 本仓库是 Agent 层：一份核心 `SKILL.md`、四个安装入口、MCP 兼容信息和版本合同。
- 不在这里复制黄雀服务端实现，也不维护四份不同的 Skill。

## 支持入口

| 入口 | 安装目标 |
| --- | --- |
| DeepSeek Harness | `~/.dsh/skills/use-huangque-cli` |
| Codex | `~/.codex/skills/use-huangque-cli` |
| OpenClaw | `~/.openclaw/skills/use-huangque-cli` |
| Pi Agent | `~/.pi/agent/skills/use-huangque-cli` |
| MCP | `hq mcp`，每项黄雀能力映射为独立工具 |

CLI 0.12.0 起统一安装并提供 MCP：

```sh
hq skill install deepseek
hq skill install codex
hq skill install openclaw
hq skill install pi
hq skill install mcp
```

重复运行同一命令会检查版本并更新受管安装。已有但不受管的同名 Skill 不会被静默覆盖。

## 模板成片示例（单条 / 批量）

先读取实时可用的模板和输入合同；不要在文档或提示中保存模板 ID、字体或价格。

```sh
hq run matrix-template-capability --json
hq run matrix-template-templates --json

# 单条：按 live describe 写入 single.json；template_id 和可选 font_family 来自上一步
hq describe matrix-template-generate --json
hq run matrix-template-generate --input @single.json --json
hq run matrix-template-generate --input @single.json --confirm --quote-token <quote_token> --json

# 批量：按 live describe 写入 batch.json，并将 count 设为 2-5
hq describe matrix-template-batch-generate --json
hq run matrix-template-batch-generate --input @batch.json --json
hq run matrix-template-batch-generate --input @batch.json --confirm --quote-token <quote_token> --json
```

每个单条或批量请求只报价一次、确认一次。保存全部返回的 `job_ids` 和原 `quote_token`；若批量部分成功或状态未知，保留已接受任务并按返回的结构化恢复指引处理，不能新建一批重试。

## B 站采集示例

```sh
hq describe collect-content --json
printf '%s' '{"url":"<BILIBILI_URL>"}' | hq run collect-content --input @-
```

第一条运行只取得服务端报价。只有用户明确同意报价后，才可用完全相同的输入加上 `--confirm --quote-token <quote_token>` 提交。

## 安全合同

- 查询、预览和报价可直接执行。
- 扣费、采集、生成、覆盖和上传必须明确确认。
- 未知状态的创建任务不得自动重试。
- MCP 不提供任意终端命令入口。
- 仓库不保存 Token、Cookie、客户数据或黄雀服务端秘密。

版本和适配目标以 [`manifest.json`](manifest.json) 为准：Skill 核心最低支持 CLI 0.10.2，并仅使用实时发现中存在的能力；本版已测试、最新和安装器目标是 0.12.0；安装入口与 MCP 需 CLI 0.12.0。Skill 独立发布，CLI 升级后重新校验兼容性，不强制共用版本号。

## 开发验证

```sh
python3 scripts/build_manifest.py --check
python3 -m unittest discover -s tests -v
```

MIT License
