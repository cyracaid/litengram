# Issue: Web API 上传的附件在 WebDAV 模式下客户端找不到文件

- **状态**: `resolved`（2026-08-13 手动重挂后关闭）
- **日期**: 2026-08-13
- **报告人**: sloblucyra
- **影响组件**: `scripts/zotero_upload.py` / Zotero 文件同步模式
- **严重性**: 中（自动上传路径产生孤儿附件）

## 症状

Zotero 客户端刷新后报：

```
The attached file could not be found at the following path:
/Users/sloblucyra/Zotero/storage/DWWREUQS/nsaf102_epmc.pdf
It may have been moved or deleted outside of Zotero, or, if the file was added
on another computer, it may not yet have been synced to zotero.org.
```

附件条目（DWWREUQS）在，云端 md5 已注册，但本地 storage 无文件、客户端拉不到。

## 根因

**存储双轨冲突**：
- `scripts/zotero_upload.py` 走 Web API → 文件进 **Zotero 云存储（S3）**
- 用户文件同步模式是 **WebDAV（坚果云）** → 客户端只从坚果云读写附件
- WebDAV 模式不认 zotero.org 的 S3 文件 → 附件变孤儿：
  云端有条目 + md5，但文件在客户端永远拉不到

误用场景：当初为解 Zotero 云配额满（413）才配的坚果云 WebDAV；
之后 `zotero_upload.py` 自动上传仍走 API（S3），两套存储没对齐。

## 修复（已验证）

手动重挂，让客户端接管文件：
1. Zotero 里删除孤儿附件（DWWREUQS）
2. 右键父条目 → 添加附件 → 附加文件的副本
3. 选 `~/Zotero/pdf-inbox/nsaf102_epmc.pdf`（`--manual` 下载的副本）
4. Zotero 复制进本地 storage + 走 WebDAV 推到坚果云

结果：客户端自行管理文件与同步，PDF 正常打开。

## 教训 / 规则

- **WebDAV 模式下不要用 `zotero_upload.py` 自动上传**（会进 S3 而不是坚果云）
- WebDAV 模式 → 用 `--manual` 下载到 inbox → 客户端手动附加
- `zotero_upload.py` 自动上传只适合 **Zotero 云存储（zotero.org File Storage）** 模式的库
- 脚本应在自动上传前检测存储协议（prefs.js `extensions.zotero.sync.storage.protocol`），
  是 `webdav` 则提示改用 `--manual`

## 候选改进（待评估）

- [x] 自动模式检测 `storage.protocol == "webdav"` → 拒绝自动上传，提示 `--manual`
      （已实现于 `zotero_upload.py` `guard_storage_protocol()`，`--force` 可覆盖）
- [x] README/文档明确：自动上传 ≠ WebDAV 模式可用
      （v1.4 修复记录 + 本 issue）

## 相关

- `docs/issues/2026-08-13-jianguoyun-webdav-503.md` — 坚果云限流（手动模式的另一动机）
