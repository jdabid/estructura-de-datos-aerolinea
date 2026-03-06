# Registro de Errores por Sprint

Documentacion de errores encontrados durante el desarrollo, sus causas raiz y soluciones aplicadas.

## Indice

| Sprint | Documento | Errores | Recurrentes |
|--------|-----------|---------|-------------|
| Sprint 1 | [sprint-1-errores.md](./sprint-1-errores.md) | 7 | 3 |
| Sprint 2 | [sprint-2-errores.md](./sprint-2-errores.md) | 5 | 2 |

## Patrones Recurrentes Detectados

| ID | Patron | Frecuencia | Skill/Solucion |
|----|--------|------------|----------------|
| REC-01 | Conflictos en archivos compartidos al merge paralelo | 6 veces (S1+S2) | Skill: `resolve-parallel-conflicts.md` |
| REC-02 | Worktree branch no se puede eliminar post-merge | 3 veces (S1+S2) | Skill: `cleanup-worktrees.md` |
| REC-03 | Agent sobreescribe archivo en vez de editar | 2 veces (S2) | Documentado en instrucciones de agents |

## Convencion

Cada error se documenta con:
- **ID**: ERR-S{sprint}-{numero}
- **Severidad**: Critica / Alta / Media / Baja
- **Estado**: Resuelto / Mitigado / Pendiente
- **Recurrente**: Si/No + referencia a patron REC-XX
