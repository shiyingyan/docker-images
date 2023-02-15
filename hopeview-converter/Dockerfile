FROM harbor.sanywind.net/scadaplus_release/hopeview_blq:1.2
# 设置服务需要拉取的配置文件
ENV CONFC_SERVICES hopeview-converter
# 设置confd
ENV CONFD_HOST confd:8000

COPY confc conf-wrapper /usr/bin/
COPY appmain.sh /app/bin/hopeview/

ENTRYPOINT ["conf-wrapper"]

CMD ["/app/bin/hopeview/appmain.sh"]