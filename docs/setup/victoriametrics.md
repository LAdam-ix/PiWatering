# VictoriaMetrics setup (Raspberry Pi, arm64)

Self-contained in one folder, `<VM_DIR>` (e.g. `~/.victoria-metrics`):

```
<VM_DIR>/
  victoria-metrics            # the binary
  victoria-metrics.service     # the unit (template in this repo)
  db/                         # -storageDataPath (snapshots auto-go to db/snapshots/)
```

## Install
1. Download the arm64 build from the VictoriaMetrics releases page
   (`victoria-metrics-linux-arm64-vX.Y.Z.tar.gz`).
2. ```
   mkdir -p <VM_DIR>/db
   tar xzf victoria-metrics-linux-arm64-*.tar.gz
   mv victoria-metrics-prod <VM_DIR>/victoria-metrics
   ```
3. Copy `victoria-metrics.service` into `<VM_DIR>` and fill in `<USER>` / `<VM_DIR>`.

## Run as a service
```
sudo systemctl enable <VM_DIR>/victoria-metrics.service   # systemd links it into /etc
sudo systemctl start victoria-metrics
```
Listens on `:8428`. App writes line protocol to `/write`; query via `/api/v1/query`.

## Backup to NAS
```
curl http://localhost:8428/snapshot/create     # snapshot -> db/snapshots/
rsync -a <VM_DIR>/ /mnt/nas/vm-backup/
```

## Notes
- `-memory.allowedPercent=50` caps RAM (~half of 512 MB on a Zero 2 W).
- `-inmemoryDataFlushInterval=60s` reduces SD-card writes.
- Keep `<VM_DIR>` under home so a whole-home rsync includes the data.
