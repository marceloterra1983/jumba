# Gates: revisão limpeza Jumba

OWNS: AGENTS.md, README.md, GATES.md, docs/**, .gitignore

Scope: Revisar ~/Projects/Jumba, limpar o seguro (paths /mnt quebrados), confirmar governança e regenerar vetores.

- [x] G1: Path canônico e worktree única (só main)
  CHECK: test -d /home/marce/Projects/Jumba && test ! -e /home/marce/Projects/Jumba/.worktrees && git -C /home/marce/Projects/Jumba worktree list | awk 'END{print NR}' | grep -qx 1 && echo WT_OK
  EXPECT: WT_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=1f44799b02bd37a2c206f5e81ed08ebf703858438ef5297f77603acbeeecda55; exit=0; EXPECT=matched; output-sha256=47fc3d15abcb7615b4a811023041bba7c07c2ae58ebe07700f591183b7095c68; output-bytes=6; shell=/bin/sh; cwd=/home/marce/Projects/Jumba; path=3fb275803ba7/32 entries

- [x] G2: AGENTS.md e .ai-memory.toml coerentes (workspace default, project jumba)
  CHECK: python3 -I -c "import tomllib, pathlib; p=pathlib.Path('/home/marce/Projects/Jumba'); t=tomllib.loads((p/'.ai-memory.toml').read_text()); a=(p/'AGENTS.md').read_text(); assert t['workspace']=='default' and t['project']=='jumba'; assert 'force-push' in a.lower() or 'force push' in a.lower() or 'sem force-push' in a.lower(); assert '.env' in a or 'secret' in a.lower(); assert 'docs/fontes/lives' in a; print('GOV_OK')"
  EXPECT: GOV_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=634a064b028a1268f2f74b06af82ffd46bac83a49356becdcf5f90dbd32349b0; exit=0; EXPECT=matched; output-sha256=04e014c59e5f904ccc0b11ce59fdfd38891746acff3430961dfda1470cb8b7b8; output-bytes=7; shell=/bin/sh; cwd=/home/marce/Projects/Jumba; path=3fb275803ba7/32 entries

- [x] G3: Nenhum path legado mnt-project-files restante no repo tracked
  CHECK: python3 -I -c "import subprocess; needle='/mnt/project-files/'+'jumba'; r=subprocess.run(['git','-C','/home/marce/Projects/Jumba','grep','-n',needle,'--','.'], capture_output=True, text=True); print('MNT_FOUND\n'+r.stdout if r.returncode==0 and r.stdout.strip() else 'MNT_CLEAN')"
  EXPECT: MNT_CLEAN
  EVIDENCE: automatic-evidence=v1; definition-sha256=0f14242e778189c83eb2348239dd94257c72aba93e5b14d5e48bb140870a9116; exit=0; EXPECT=matched; output-sha256=c7d2ee3c73402a61fe2f9608e83e1f273241630d460c24f1ea7ea8fca78c1f0e; output-bytes=10; shell=/bin/sh; cwd=/home/marce/Projects/Jumba; path=3fb275803ba7/32 entries

- [x] G4: Geradores de vetores regeneram sem erro (oficial deste repo)
  CHECK: python3 -I /home/marce/Projects/Jumba/docs/vetores/geradores/gera_precificacao.py --saida /home/marce/Projects/Jumba/docs/vetores/ --espera 0 >/tmp/jumba-prec.json && python3 -I /home/marce/Projects/Jumba/docs/vetores/geradores/gerar_agregados.py --saida /home/marce/Projects/Jumba/docs/vetores/ --feriados-json /home/marce/Projects/Jumba/docs/conhecimento/b3-outros/feriados-b3-2026-2028.json >/tmp/jumba-agr.out && python3 -I /home/marce/Projects/Jumba/docs/conhecimento/b3-outros/scripts/gerar_calendario.py /home/marce/Projects/Jumba/docs/conhecimento/b3-outros/feriados-b3-2026-2028.json >/tmp/jumba-cal.out && echo VETORES_OK
  EXPECT: VETORES_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=e91fe00f9262367768d64969960530e744af18ebed92e7cdca1d46b0da003bab; exit=0; EXPECT=matched; output-sha256=15bc4a58576fbd87189490de4202eb0a1e53a0e3b1802585811e757af737d4f5; output-bytes=11; shell=/bin/sh; cwd=/home/marce/Projects/Jumba; path=3fb275803ba7/32 entries

- [x] G5: Inventário lives: 8 .txt + RESUMO; audio ignorado pelo git
  CHECK: python3 -I -c "from pathlib import Path; L=Path('/home/marce/Projects/Jumba/docs/fontes/lives'); txts=sorted(L.glob('*.txt')); assert len(txts)==8, len(txts); assert (L/'RESUMO.md').is_file(); import subprocess; r=subprocess.check_output(['git','-C',str(L.parents[2]),'check-ignore','-v','docs/fontes/lives/audio/'], text=True); assert 'audio' in r; print('LIVES_OK')"
  EXPECT: LIVES_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=6c2766dc902a01262d5eea23afb42752cec1332485792a5d8c90c878fbee6e5d; exit=0; EXPECT=matched; output-sha256=4f4275895f35058e264d763362bbc0be23e50391ff8db526e1867aacbebde61f; output-bytes=9; shell=/bin/sh; cwd=/home/marce/Projects/Jumba; path=3fb275803ba7/32 entries

- [x] G6: Sem secrets óbvios rastreados
  CHECK: python3 -I -c "import subprocess,re; out=subprocess.check_output(['git','-C','/home/marce/Projects/Jumba','ls-files'], text=True); bad=[f for f in out.splitlines() if f.endswith('.env') or 'credentials' in f.lower() or f.endswith('.pem')]; assert not bad, bad; print('SECRETS_OK')"
  EXPECT: SECRETS_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=3ae581d597da1cea169760ec3bcdf7c48a7496b793705099440419a5d5b1485b; exit=0; EXPECT=matched; output-sha256=0c41d67e93d1f0a1b37c953705ff51caf0e4e1233367151bf3bb77cf39fb2081; output-bytes=11; shell=/bin/sh; cwd=/home/marce/Projects/Jumba; path=3fb275803ba7/32 entries
