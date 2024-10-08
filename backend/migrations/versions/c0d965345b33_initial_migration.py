"""Initial migration

Revision ID: c0d965345b33
Revises: 
Create Date: 2024-09-26 12:38:27.669346

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0d965345b33'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('survey_data', schema=None) as batch_op:
        # Add the timestamp column
        batch_op.add_column(sa.Column('timestamp', sa.DateTime(), nullable=True))
        
        # Add a temporary column
        batch_op.add_column(sa.Column('temp_user_id', sa.String(length=64), nullable=True))
        
        # Update the temporary column with a default value where user_id is null
        op.execute("UPDATE survey_data SET temp_user_id = COALESCE(user_id, 'default_user_id')")
        
        # Drop the old user_id column
        batch_op.drop_column('user_id')
        
        # Add the new user_id column as non-nullable
        batch_op.add_column(sa.Column('user_id', sa.String(length=64), nullable=False, server_default='default_user_id'))
        
        # Copy data from temp_user_id to user_id
        op.execute("UPDATE survey_data SET user_id = temp_user_id")
        
        # Drop the temporary column
        batch_op.drop_column('temp_user_id')
        
        # Make session_id nullable
        batch_op.alter_column('session_id',
               existing_type=sa.VARCHAR(length=64),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('survey_data', schema=None) as batch_op:
        batch_op.alter_column('session_id',
               existing_type=sa.VARCHAR(length=64),
               nullable=False)
        batch_op.drop_column('timestamp')
        
        # Make user_id nullable again
        batch_op.alter_column('user_id', nullable=True)

    # ### end Alembic commands ###