# Issue: 坚果云 WebDAV 503 BlockedTemporarily 限流

- **状态**: `open`
- **日期**: 2026-08-13
- **报告人**: sloblucyra
- **影响组件**: `zotero_upload.py` / Zotero 文件同步（WebDAV → 坚果云）
- **严重性**: 中（阻塞附件云同步，不影响 annotation 元数据同步）

## 症状

Zotero 同步时报大量 503：

```
HTTP GET https://dav.jianguoyun.com/dav/zotero/{KEY}.prop failed with status code 503:
<d:error xmlns:d="DAV:" xmlns:s="http://ns.jianguoyun.com">
  <s:exception>BlockedTemporarily</s:exception>
  <s:message>Too many requests are received recently</s:message>
</d:error>
[JavaScript Error: "Failed too many times"]
[JavaScript Error: "Upload request 1/{KEY} failed"]
[JavaScript Error: "Download request 1/{KEY} failed"]
```

报错 key 示例：`DWWREUQS`、`Z9265VUY`、`ZBCAEDES`、`ZDIAQWXC`、`ZNGGDYA2`、`ZTMZQ73B`。

## 根因

**坚果云官方限流**，非配置/认证错误：
- 免费版 WebDAV 有严格请求速率限制（约 30 秒内数十请求）
- Zotero 对每个附件发多个请求（`.prop` 检查 + 上传/下载）
- 库中 400+ 附件，首次全量同步瞬间打爆限流
- 认证已通过（URL 含账号、能走到限流即密码 OK）

## 排查过程

- 配置本身有效：`extensions.zotero.sync.storage.url = dav.jianguoyun.com/dav`，
  `verified=true`，`Zotero-API-Key` 上传 S3 正常
- WebDAV 限流错误 XML 特征：`<s:exception>BlockedTemporarily</s:exception>`
- Zotero 指数退避会自动重试，但反复点同步会加重限流

## 当前影响

- 附件（PDF）云端同步受阻——Zotero 云配额满时依赖 WebDAV 存附件
- annotation 元数据同步走 zotero.org API，**不受影响**（已验证 80 条 annotation 上云成功）

## 缓解措施（已验证）

1. 停 5-10 分钟触发重试（坚果云限流窗口自动恢复）
2. 不要狂点同步——让 Zotero 指数退避自动跑
3. 首次全量同步会分批慢爬，属正常

## 候选方案（待评估）

- [ ] **A** 升级坚果云付费档（速率更高）
- [ ] **B** 关闭 Zotero 文件同步，附件只留本地（annotation 照常）
- [ ] **C** 换成其他 WebDAV（Box 10GB / Nextcloud 自建）
- [ ] **D** 在 `zotero_upload.py` 中检测 503 BlockedTemporarily → 提示用户等待限流窗口 + 指数退避重试

## 相关

- 前置事故链：Zotero key 非法 → 400 `not a valid item key`（v1.3 已修复）
- 本 issue 与 key 问题独立，属坚果云服务端限制
