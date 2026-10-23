# Dataset access and handling

## What the code expects

The final evaluation reads this exact relative path when run from `src`:

```text
../data/wustl-ehms-2020_with_attacks_categories.csv
```

The local source folder contained a 3,946,888-byte, 45-column file of that
name. The `*_with_attacks_categories.csv` name indicates an annotated variant,
but the local project does not contain a verified provenance record or a
script that creates that exact variant from an official download.

## Source, license, and redistribution

The dataset's official landing-page URL, version, license, and permission to
redistribute the local annotated copy could not be verified from project
materials. The dataset is therefore not copied into this repository. Before
use or public distribution:

1. Locate the dataset through its official publisher/university source.
2. Confirm the applicable license and any terms for redistribution or derived
   labels; do not rely on copies hosted by unrelated repositories.
3. Confirm the provenance and transformation that added the `Attack Category`
   column to the original dataset.
4. Review the file for privacy and re-identification risk. The local CSV
   schema includes `SrcAddr`, `DstAddr`, `SrcMac`, and `DstMac`.
5. Place only a permitted, appropriately reviewed file at the expected path.

Do not commit the dataset unless the rights holder's permission and privacy
review explicitly permit it. The code drops several address and MAC fields
before modeling, but this does not make redistribution of the raw file safe.

## Expected columns

See [`../docs/data_dictionary.md`](../docs/data_dictionary.md) for the field
names and preprocessing behavior currently assumed by the scripts. The code
expects `Packet_num`, `Attack Category`, and `Label`; field names and label
semantics should be checked against the exact obtained dataset.
