# MOxing1/rule

Mihomo / Clash Meta 的自定义规则生成器配置，供 `rule.ini` 使用。

## 分流原则

1. **中国大陆服务优先直连**：包括 Kimi、DeepSeek、智谱、通义、豆包、文心、混元等，集中维护在 `AI_CN.list`。
2. **海外 AI 单独代理**：ChatGPT、Claude、Gemini、Perplexity、Grok、Mistral、OpenRouter 等由 `AI.list` 进入 `🤖 AI` 策略组。
3. **GitHub 与 Copilot 分离**：普通 GitHub 流量使用 `GitHub` 组；Copilot API、遥测和代理端点使用 `Copilot` 组，避免把整个 GitHub 强制归入 Copilot。
4. **规则顺序优先于策略组名称**：`rule.ini` 中越靠前的规则优先匹配。国内 AI 直连规则位于海外 AI 规则之前。
5. **避免宽泛公共依赖域名**：不再把整个 `auth0.com`、`stripe.com`、`sentry.io` 等公共服务域名粗暴归入 AI，减少无关流量误代理。

## 文件说明

- `rule.ini`：规则集和策略组定义。
- `AI_CN.list`：中国大陆 AI 服务直连规则。
- `AI.list`：海外 AI 服务代理规则。
- `Copilot.list`：GitHub Copilot 专用端点规则。
- `Direct.list`：其他国内域名、局域网和直连补充规则。
- `ProxyLite.list`：海外 DNS 和少量补充代理规则。

## 维护约定

- 新增中国大陆 AI 服务时，只加入 `AI_CN.list`，不要放进 `AI.list`。
- 新增海外 AI 服务时，只加入 `AI.list`，并确认没有被 `AI_CN.list` 或 `Direct.list` 覆盖。
- 不使用 `DOMAIN-KEYWORD` 代替明确的 `DOMAIN` / `DOMAIN-SUFFIX`，除非确实无法枚举域名。
- 不把整个公共基础设施域名加入单一业务策略组。
- 修改后运行：

```bash
python3 scripts/validate_rules.py
```

## 兼容性

规则采用 Clash classical list 语法，并通过 `rule-generator` 的 `ruleset=` 与 `custom_proxy_group=` 配置生成最终订阅。远程规则文件使用 GitHub Raw 地址。
