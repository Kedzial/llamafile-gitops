# llamafile-gitops

Potok CI/CD oraz deklaratywna konfiguracja wdrożenia usługi `llamafile` na klastrze `k3s` (NixOS) z wykorzystaniem GitHub Actions i Ansible.

## Struktura projektu
- `src/` — moduły klienta API oraz funkcje pomocnicze
- `tests/` — testy jednostkowe (`pytest`)
- `k8s/` — manifesty Kubernetesa (`Deployment`, `Service`, `ConfigMap`)
- `ansible/` — konfiguracja maszyny produkcyjnej NixOS i runnera `self-hosted`
- `.github/workflows/` — definicja potoku CI/CD
