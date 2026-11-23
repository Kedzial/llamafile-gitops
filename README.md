# llamafile-gitops

Potok CI/CD oraz deklaratywna konfiguracja wdrożenia usługi `llamafile` na klastrze `k3s` (NixOS) z wykorzystaniem GitHub Actions i Ansible.

## Struktura projektu
- `src/` — moduły klienta API oraz funkcje pomocnicze
- `tests/` — testy jednostkowe (`pytest`)
- `k8s/` — manifesty Kubernetesa (`Deployment`, `Service`, `ConfigMap`)
- `ansible/` — konfiguracja maszyny produkcyjnej NixOS i runnera `self-hosted`
- `.github/workflows/` — definicja potoku CI/CD

# Dokumentacja projektu: llamafile-gitops

## 1. Architektura rozwiązania
Projekt realizuje wdrożenie usługi wnioskowania LLM opartej o `llamafile` na klastrze Kubernetes (`k3s`) z wykorzystaniem praktyk DevOps/GitOps.

Przepływ procesu:
1. **Kod i Pull Request:** Programista wprowadza zmiany na osobnej gałęzi (`feat/*`) i otwiera Pull Request do `main`.
2. **Continuous Integration (GitHub-hosted runner):** Uruchamiana jest walidacja kodu (`ruff`), testy jednostkowe (`pytest`), analiza `Dockerfile` (`hadolint`) oraz walidacja manifestów K8s (`kubeconform`).
3. **Build & Push (po scaleniu do `main`):** Budowany jest obraz kontenera oznaczony tagiem `ghcr.io/kedzial/llamafile-gitops:<commit-sha>` i publikowany w GitHub Container Registry.
4. **Continuous Deployment (Self-hosted runner na NixOS):** Lokalny runner (`nixos-prod-runner`) aktualizuje tag obrazu w `k8s/deployment.yaml`, aplikuje manifesty w `k3s` i monitoruje wdrożenie (`kubectl rollout status`). W przypadku przekroczenia limitu czasu (300s) następuje automatyczny powrót do poprzedniej rewizji (`kubectl rollout undo`).

## 2. Struktura repozytorium
- `src/` — kod źródłowy klienta API oraz moduły pomocnicze aplikacji.
- `tests/` — testy jednostkowe (`pytest`) weryfikujące logikę aplikacji.
- `k8s/` — manifesty Kubernetesa (`Deployment`, `Service`, `ConfigMap`) definiujące usługę na porcie `8080`.
- `ansible/` — deklaratywna konfiguracja maszyny produkcyjnej NixOS (`inventory.ini`, `playbook.yml`, `configuration.nix.j2`).
- `.github/workflows/ci-cd.yml` — definicja potoku CI/CD w GitHub Actions.

## 3. Etapy potoku CI/CD

| Etap (Job) | Wyzwalacz (Trigger) | Środowisko | Wykonywane zadania |
| :--- | :--- | :--- | :--- |
| `lint-and-test` | `pull_request`, `push` (`main`) | `ubuntu-latest` | `ruff check`, `ruff format --check`, `pytest --cov`, `hadolint`, `kubeconform` |
| `build-and-push` | `push` (`main`) | `ubuntu-latest` | Budowa obrazu Docker i publikacja w `ghcr.io` z tagiem SHA commitu |
| `deploy-prod` | `push` (`main`) | `self-hosted` (NixOS VM) | Podmiana tagu obrazu, `kubectl apply -f k8s/`, weryfikacja `rollout status` lub `rollout undo` |

## 4. Weryfikacja działania i scenariusze testowe
W ramach testów potwierdzono poprawne działanie wszystkich mechanizmów ochronnych:
- **Blokada wadliwego kodu (CI Gate):** Próba scalenia kodu niespełniającego reguł formatowania (`ruff format`) zatrzymała potok na pierwszym etapie, pomijając budowę obrazu i wdrożenie.
- **Automatyczny Rollback (CD):** Symulacja błędu pobierania obrazu / przekroczenia czasu oczekiwania wyzwoliła automatyczne wycofanie zmiany (`kubectl rollout undo deployment/llamafile-deployment`), zachowując ciągłość działania poprzedniej repliki.
- **Praca zespołowa i Rolling Update:** Po akceptacji Pull Requestów i scaleniu zmian od wielu kolaborantów klaster `k3s` przeprowadził bezprzerwową podmianę kontenerów (`deployment "llamafile-deployment" successfully rolled out`), a usługa odpowiada poprawnie pod adresem `http://192.168.100.162:8080/v1/models`.
