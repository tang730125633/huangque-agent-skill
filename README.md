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

CLI 0.11.0 起统一安装：

```sh
hq skill install deepseek
hq skill install codex
hq skill install openclaw
hq skill install pi
hq skill install mcp
```

重复运行同一命令会检查版本并更新受管安装。已有但不受管的同名 Skill 不会被静默覆盖。

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

版本和适配目标以 [`manifest.json`](manifest.json) 为准。Skill 独立发布，CLI 升级后重新校验兼容性，不强制共用版本号。

## 开发验证

```sh
python3 scripts/build_manifest.py --check
python3 -m unittest discover -s tests -v
```

MIT License
