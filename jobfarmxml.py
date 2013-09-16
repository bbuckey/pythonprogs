from simplehttpclient import post

class JFXML:

    def __init__(self):
        self.xml = ""

    def exchange(self, procid, infile):
        self.xml = """
<ServiceRequest>
    <service class="service.PropertiesDrivenService">
        <properties>
            <property name="PROCESS_ID" value="%s"/>
        </properties>
        <className>service.Clasd</className>
    </service>
    <requester>DATASYNC</requester>
</ServiceRequest>""" % (procid, infile)
        return self


    def stage(self, procid, exchfile):
        self.xml = """
<ServiceRequest>
    <service class="service.PropertiesDrivenService">
        <properties>
            <property name="PROCESS_ID" value="%s"/>
            <property name="imaxImportFileName" value="%s"/>
            <property name="carrier" value="ibc"/>
        </properties>
        <className>service.ImportStageActionImpl</className>
    </service>
    <requester>DATASYNC</requester>
</ServiceRequest>""" % (procid, exchfile)
        return self

    def recon(self, procid, fileid):
        self.xml = """
<ServiceRequest>
    <service class="com.benefitfocus.automation.jobfarm.PropertiesDrivenService">
        <properties>
            <property name="PROCESS_ID" value="%s"/>
            <property name="fileID" value="%s"/>
            <property name="carrier" value="ibc"/>
        </properties>
        <className>com.benefitfocus.automation.ie.action.ImaxReconStageActionImpl</className>
    </service>
    <requester>DATASYNC</requester>
</ServiceRequest>""" % (procid, fileid)
        return self

    def aqp(self, procid, fileid):
        self.xml = """
<ServiceRequest>
    <service class="com.benefitfocus.automation.jobfarm.PropertiesDrivenService">
        <properties>
            <property name="PROCESS_ID" value="%s"/>
            <property name="fileID" value="%s"/>
            <property name="carrier" value="ibc"/>
        </properties>
        <className>com.benefitfocus.automation.ie.action.ImaxActionQueueProcessorActionImpl</className>
    </service>
    <requester>DATASYNC</requester>
</ServiceRequest>""" % (procid, fileid)
        return self


# ---------------------- GMAX

    def gmaxExchange(self, procid, infile):
        self.xml = """
        <ServiceRequest>
            <service class="com.benefitfocus.automation.jobfarm.PropertiesDrivenService">
                <properties>
                    <property name="PROCESS_ID" value="pid-%s"/>
                    <property name="inbound.file" value="%s"/>
                    <property name="customer.code" value="ibc"/>
                </properties>
                <className>com.benefitfocus.gmax2.automation.GmaxAutomationImpl</className>
            </service>
            <requester>DATASYNC</requester>
        </ServiceRequest>
        """ % (procid, infile)
        
        return self

    
    def gmaxStage(self, procid, exchfile):
        self.xml = """
        <ServiceRequest>
            <service class="com.benefitfocus.automation.jobfarm.PropertiesDrivenService">
                <properties>
                    <property name="PROCESS_ID" value="JOBFARM BENCHMARK %s"/>
                    <property name="gmaxImportFileName" value="%s"/>
                    <property name="carrier" value="ibc"/>
                </properties>
                <className>com.benefitfocus.automation.ie.action.GmaxImportStageActionImpl</className>
            </service>
            <requester>DATASYNC</requester>
        </ServiceRequest>
        """ % (procid, exchfile)
       
        return self
    
    def gmaxRecon(self, procid, fileid):
        self.xml = """
        <ServiceRequest>
            <service class="com.benefitfocus.automation.jobfarm.PropertiesDrivenService">
                <properties>
                    <property name="PROCESS_ID" value="pid-%s"/>
                </properties>
                <className>com.benefitfocus.automation.ie.action.GmaxReconStageActionImpl</className>
            </service>
            <requester>BFDMACE</requester>
        </ServiceRequest>
        """ % (procid, fileid)
        
        return self
        
    def gmaxAqp(self, procid, fileid):
        self.xml = """
        <ServiceRequest>
            <service class="com.benefitfocus.automation.jobfarm.PropertiesDrivenService">
                <properties>
                    <property name="PROCESS_ID" value="pid-%s"/>
                </properties>
                <className>com.benefitfocus.automation.ie.action.GmaxActionQueueProcessorActionImpl</className>
            </service>
            <requester>DATASYNC</requester>
        </ServiceRequest>
        """ % (procid, fileid)
        
        return self
    
    def withCallback(self, callback):
        self.xml = self.xml.replace("</ServiceRequest>", """<callbacks>
        <string>%s</string>
    </callbacks>    
</ServiceRequest>""" % callback)
        return self

    
            
    def __str__(self):
        return self.xml
        
    
if __name__ == "__main__":

    server = "localhost:8080"
    callback = "localhost:8182"
    
    print post(server, "/queue/exchange-jct", str(JFXML().exchange().withCallback(callback)))
    print post(server, "/queue/imax-stage-jct", str(JFXML().stage().withCallback(callback)))
    print post(server, "/queue/imax-recon-jct", str(JFXML().recon().withCallback(callback)))
    print post(server, "/queue/imax-aqp-jct", str(JFXML().aqp().withCallback(callback)))
    
    
