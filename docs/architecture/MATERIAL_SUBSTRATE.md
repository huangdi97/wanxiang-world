# Material Substrate (G02C)

Ownership: `wanxiang_substrate.material` (items, containers, custody, ownership,
information payloads); framework-free domain semantics.

## Model

- `MaterialItem`: immutable identity, kind, state (intact/damaged/consumed).
- `ContainerSpec`: capacity + accepted kinds; nested containment.
- `Custody` vs `Ownership`: physical possession is distinct from legal ownership.
- `InfoPayload`: sealed/read + readers list ? custody never equals knowledge.

## Authority

Material changes are resolvers through the M1 Commit Authority:
- `material.create_item` / `material.create_container`,
- `material.transfer` (non-custodian -> `NotCustodian`; consumed -> rejected),
- `material.move_into_container` (full -> `ContainerFull`; incompatible kind;
  containment cycle -> `ContainmentCycle`),
- `material.consume` / `material.damage` (explicit state transitions),
- `material.seal_payload` / `material.read_payload` (only the custodian reads;
  repeat -> `PayloadAlreadyRead`),
- `material.give_ownership`, `material.instantiate`.

## Epistemic separation

Acquiring a sealed letter (custody) does not reveal its payload. Reading is an
explicit action by the custodian; readers are recorded on the payload component.

## Compatibility

- Material state rides on versioned components (`material` schema v1); no new
  migration; M1 replay untouched.
- Object custody/ownership history reconstructs independently per branch.
