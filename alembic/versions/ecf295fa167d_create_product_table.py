
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ecf295fa167d'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'dummy_table',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length = 100), nullable= False),
        sa.Column('created_at', sa.DateTime(), server_default = sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default = sa.func.now())
    )



def downgrade() -> None:
    op.drop_table('dummy_table')
