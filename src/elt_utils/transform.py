from pyspark.sql import DataFrame
from pyspark.sql.functions import col
from pyspark.sql.types import StructType


def normalize_schema(df: DataFrame, schema: StructType) -> DataFrame:
    """
    Aplica um schema a um DataFrame existente, fazendo cast das colunas conforme os tipos definidos.

    Args:
        df (DataFrame): DataFrame de entrada.
        schema (StructType): Schema esperado com nomes e tipos das colunas.

    Returns:
        DataFrame: DataFrame com colunas convertidas para os tipos do schema.
    """
    columns_casted = []

    for field in schema.fields:
        if field.name in df.columns:
            columns_casted.append(col(field.name).cast(field.dataType).alias(field.name))
        else:
            # Adiciona coluna nula com tipo correto, se não estiver presente
            from pyspark.sql.functions import lit
            columns_casted.append(lit(None).cast(field.dataType).alias(field.name))

    return df.select(*columns_casted)
