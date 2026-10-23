# Expected CSV fields and preprocessing

This is a code-derived schema description, not an authoritative dictionary
from the dataset publisher. In the inspected local CSV, the header had 45
fields:

```text
Dir, Flgs, SrcAddr, DstAddr, Sport, Dport, SrcBytes, DstBytes, SrcLoad,
DstLoad, SrcGap, DstGap, SIntPkt, DIntPkt, SIntPktAct, DIntPktAct,
SrcJitter, DstJitter, sMaxPktSz, dMaxPktSz, sMinPktSz, dMinPktSz, Dur,
Trans, TotPkts, TotBytes, Load, Loss, pLoss, pSrcLoss, pDstLoss, Rate,
SrcMac, DstMac, Packet_num, Temp, SpO2, Pulse_Rate, SYS, DIA, Heart_rate,
Resp_Rate, ST, Attack Category, Label
```

## Fields used for ordering, labels, or category evaluation

- `Packet_num`: rows are sorted ascending before chronological splitting.
- `Label`: used to identify normal and attack rows/windows; it is removed from
  the model input.
- `Attack Category`: mapped to `spoofing`, `data alteration`, or `normal` for
  experiment grouping; its column is removed from the model input.

`Attack Category` values containing `spoof` map to `spoofing`; values
containing `alter` or `inject` map to `data alteration`; all other values map
to `normal`.

## Fields excluded from model input

The scripts explicitly drop the following if present:

- Constant or selected fields: `Dport`, `SrcGap`, `DstGap`, `DIntPktAct`,
  `dMinPktSz`, `Trans`.
- Identifier-like fields: `SrcAddr`, `DstAddr`, `SrcMac`, `DstMac`,
  `Packet_num`, `Sport`.
- Any column whose name contains `attack`, plus `Label` and derived `Cat`.

Remaining object/category columns are one-hot encoded; the resulting matrix is
standardized. The scaler is fit on normal rows in the first 70% of sorted rows.
However, one-hot encoding is performed on the full data before the split;
therefore the feature vocabulary can reflect values in later partitions.

## Important

No authoritative descriptions, units, label definitions, or provenance for the
custom annotated file were present locally. Verify them with the dataset
publisher and the creator of the annotated variant before making scientific
claims or publishing a derived data dictionary.
